"""ViT line encoder (shared by MAE pretraining and CTC fine-tuning).

Input [B, 1, 64, W], W a multiple of 8. Patches are 16 x 8 px, so a line is
a grid of 4 rows x W/8 columns of tokens. Positions use fixed 2-D sin/cos
embeddings, so a model pretrained on fixed-width crops runs on any width.

ViTLineCTC: encoder -> per column concat the 4 row tokens -> linear to
2 x n_classes (two CTC frames per 8-px column, i.e. T = W/4 like the CRNN).
"""
import math

import torch
import torch.nn as nn
import torch.nn.functional as Fn

PH, PW, ROWS = 16, 8, 4


def sincos_2d(rows, cols, dim, device):
    """[rows*cols, dim] fixed 2-D sin/cos position embedding (half dims per axis)."""
    def axis(n, d):
        pos = torch.arange(n, device=device, dtype=torch.float32)[:, None]
        omega = torch.exp(torch.arange(0, d, 2, device=device, dtype=torch.float32) * (-math.log(10000.0) / d))
        e = torch.zeros(n, d, device=device)
        e[:, 0::2] = torch.sin(pos * omega)
        e[:, 1::2] = torch.cos(pos * omega)
        return e
    er, ec = axis(rows, dim // 2), axis(cols, dim // 2)
    return torch.cat([er[:, None, :].expand(rows, cols, -1), ec[None, :, :].expand(rows, cols, -1)], -1).reshape(
        rows * cols, dim)


class Block(nn.Module):
    def __init__(self, dim, heads, mlp=4.0, drop=0.0):
        super().__init__()
        self.n1 = nn.LayerNorm(dim)
        self.qkv = nn.Linear(dim, 3 * dim)
        self.proj = nn.Linear(dim, dim)
        self.n2 = nn.LayerNorm(dim)
        self.mlp = nn.Sequential(nn.Linear(dim, int(dim * mlp)), nn.GELU(), nn.Linear(int(dim * mlp), dim))
        self.heads = heads
        self.drop = drop

    def forward(self, x, mask=None):
        """mask: optional bool [B, 1, 1, N], True = real token (padding is never attended to)."""
        B, N, D = x.shape
        q, k, v = self.qkv(self.n1(x)).reshape(B, N, 3, self.heads, D // self.heads).permute(2, 0, 3, 1, 4)
        a = Fn.scaled_dot_product_attention(q, k, v, attn_mask=mask, dropout_p=self.drop if self.training else 0.0)
        x = x + self.proj(a.transpose(1, 2).reshape(B, N, D))
        return x + self.mlp(self.n2(x))


class LineEncoder(nn.Module):
    def __init__(self, dim=256, depth=8, heads=8, drop=0.0):
        super().__init__()
        self.patch = nn.Conv2d(1, dim, kernel_size=(PH, PW), stride=(PH, PW))
        self.blocks = nn.ModuleList([Block(dim, heads, drop=drop) for _ in range(depth)])
        self.norm = nn.LayerNorm(dim)
        self.dim = dim

    def tokens(self, x):
        """Patchify + position: [B, ROWS*C, D] (row-major), and C."""
        t = self.patch(x)  # B, D, 4, C
        B, D, R, C = t.shape
        t = t.flatten(2).transpose(1, 2)  # B, R*C, D
        return t + sincos_2d(R, C, D, x.device)[None], C

    def run(self, t, mask=None):
        for b in self.blocks:
            t = b(t, mask)
        return self.norm(t)

    @staticmethod
    def key_mask(widths, C, device):
        """[B, 1, 1, ROWS*C] bool: token column < ceil(width / PW)."""
        if widths is None:
            return None
        valid = torch.div(widths.to(device) + PW - 1, PW, rounding_mode="floor").clamp(1, C)
        cols = torch.arange(C, device=device).repeat(ROWS)  # row-major token order
        return (cols[None] < valid[:, None])[:, None, None, :]

    def forward(self, x, widths=None):
        t, C = self.tokens(x)
        return self.run(t, self.key_mask(widths, C, x.device)), C


class ViTLineCTC(nn.Module):
    """head="linear": per-column linear layer (first pilot runs).
    head="lstm": project the column features, then a 2-layer BiLSTM over the
    valid columns only (packed, so padding never enters the recurrence), then
    the linear layer. Same sequence model as the CRNN baseline."""

    def __init__(self, n_classes, dim=256, depth=8, heads=8, drop=0.1, head="linear", hidden=256):
        super().__init__()
        self.encoder = LineEncoder(dim, depth, heads, drop)
        self.drop = nn.Dropout(drop)
        self.head_type = head
        if head == "lstm":
            self.proj = nn.Linear(ROWS * dim, hidden)
            self.rnn = nn.LSTM(hidden, hidden, num_layers=2, bidirectional=True, dropout=0.25, batch_first=True)
            self.head = nn.Linear(2 * hidden, 2 * n_classes)
        else:
            self.head = nn.Linear(ROWS * dim, 2 * n_classes)
        self.n_classes = n_classes
        self.stride = PW // 2

    def column_features(self, x, widths=None):
        h, C = self.encoder(x, widths)  # B, 4*C, D
        B, _, D = h.shape
        return h.reshape(B, ROWS, C, D).permute(0, 2, 1, 3).reshape(B, C, ROWS * D)  # B, C, 4D

    def features(self, x, widths=None):
        """[B, D', T] for invariance scores (same convention as CRNN.features)."""
        return self.column_features(x, widths).transpose(1, 2)

    def forward(self, x, widths=None):
        f = self.column_features(x, widths)
        B, C, _ = f.shape
        if self.head_type == "lstm":
            f = self.drop(self.proj(f))
            # the recurrence runs in fp32: a packed LSTM under bf16 autocast did not train
            with torch.autocast("cuda", enabled=False):
                f = f.float()
                if widths is not None:
                    lens = torch.div(widths + PW - 1, PW, rounding_mode="floor").clamp(1, C).cpu()
                    packed = nn.utils.rnn.pack_padded_sequence(f, lens, batch_first=True, enforce_sorted=False)
                    h, _ = self.rnn(packed)
                    f, _ = nn.utils.rnn.pad_packed_sequence(h, batch_first=True, total_length=C)
                else:
                    f, _ = self.rnn(f)
        o = self.head(self.drop(f)).reshape(B, C * 2, self.n_classes)  # two frames per column
        return o.float().log_softmax(-1).transpose(0, 1)  # T, B, C

    def out_lengths(self, widths):
        return torch.div(widths, self.stride, rounding_mode="floor").clamp(min=1)

    def load_encoder(self, path):
        sd = torch.load(path, map_location="cpu")
        sd = {k[len("encoder."):]: v for k, v in sd.items() if k.startswith("encoder.")} or sd
        return self.encoder.load_state_dict(sd, strict=False)

    def set_encoder_trainable(self, flag):
        for p in self.encoder.parameters():
            p.requires_grad_(flag)
