"""Convolutional masked (denoising) autoencoder on the CRNN's own CNN encoder.

Why: the pilot's small ViT memorised the few labelled lines (train loss ~0,
test CER ~60%) and its MAE features were weak at our data scale, while the
CRNN generalises well. So the pretraining under study (rebuild clean lines
from masked + corrupted ones) is applied to the CRNN's CNN instead, in the
spirit of fully convolutional MAEs for handwriting (Text-MAE).

Masking: random vertical strips of STRIP px (MASK_RATIO of the strips) are
blanked in the INPUT (set to 0 = paper). The CNN (identical to CRNN.cnn,
output [B, 384, 1, W/4]) encodes the line; a light decoder (two 1-D convs)
predicts the CLEAN pixels of every 64 x 4 column. Loss = MSE on masked
columns + VIS_W x MSE on visible columns (same weighting as the ViT MAE).

The encoder state dict uses the CRNN's "cnn.*" keys, so CRNN.load_encoder()
loads it directly for fine-tuning.
"""
import torch
import torch.nn as nn

from lwti.models.crnn import CRNN

COL = 4          # CNN output stride: one feature column per 4 px
STRIP = 8        # masking granularity in px (2 feature columns)
VIS_W = 0.25


class ConvMAE(nn.Module):
    def __init__(self, mask_ratio=0.6, height=64):
        super().__init__()
        self.cnn = CRNN(n_classes=2).cnn  # same layers and keys as the recogniser's encoder
        self.dec = nn.Sequential(
            nn.Conv1d(384, 384, 5, padding=2), nn.GELU(),
            nn.Conv1d(384, 384, 5, padding=2), nn.GELU(),
            nn.Conv1d(384, height * COL, 1),
        )
        self.mask_ratio = mask_ratio
        self.H = height

    @staticmethod
    def patchify(x):
        """[B,1,H,W] -> [B, W/4, H*4] column patches."""
        B, _, H, W = x.shape
        return x.reshape(B, H, W // COL, COL).permute(0, 2, 1, 3).reshape(B, W // COL, H * COL)

    @staticmethod
    def unpatchify(p, H, W):
        B = p.shape[0]
        return p.reshape(B, W // COL, H, COL).permute(0, 2, 1, 3).reshape(B, 1, H, W)

    def forward(self, x_in, x_clean):
        B, _, H, W = x_in.shape
        n_strips = W // STRIP
        m = (torch.rand(B, n_strips, device=x_in.device) < self.mask_ratio).float()  # 1 = masked
        m_px = m.repeat_interleave(STRIP, dim=1)[:, None, None, :]  # B,1,1,W
        x_masked = x_in * (1 - m_px)
        f = self.cnn(x_masked).squeeze(2)  # B, 384, W/4
        pred = self.dec(f).transpose(1, 2).float()  # B, W/4, H*4
        target = self.patchify(x_clean).float()
        err = ((pred - target) ** 2).mean(-1)  # B, W/4
        masked = m.repeat_interleave(STRIP // COL, dim=1)  # per feature column
        loss = (err * masked).sum() / masked.sum().clamp(min=1) + \
            VIS_W * (err * (1 - masked)).sum() / (1 - masked).sum().clamp(min=1)
        return loss, pred, masked

    def encoder_state(self):
        return {"cnn." + k: v for k, v in self.cnn.state_dict().items()}
