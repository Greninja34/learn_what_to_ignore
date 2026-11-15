"""Masked autoencoder for text lines (optionally denoising).

The encoder sees the visible 25% of the tokens of the INPUT line (clean for
plain MAE, corrupted for the damage variants); a light decoder predicts the
pixels of the CLEAN line for every token. Loss = MSE on masked tokens
+ VIS_W * MSE on visible tokens (the same weight for every variant, so the
only difference between runs is the corruption setting).

Inputs are fixed-width crops [B, 1, 64, CROP_W] with ink = 1.
"""
import torch
import torch.nn as nn

from lwti.models.vit_line import PH, PW, Block, LineEncoder, sincos_2d

VIS_W = 0.25


class LineMAE(nn.Module):
    def __init__(self, dim=256, depth=8, heads=8, dec_dim=192, dec_depth=4, dec_heads=6, mask_ratio=0.75):
        super().__init__()
        self.encoder = LineEncoder(dim, depth, heads)
        self.enc_to_dec = nn.Linear(dim, dec_dim)
        self.mask_token = nn.Parameter(torch.zeros(1, 1, dec_dim))
        self.dec = nn.ModuleList([Block(dec_dim, dec_heads) for _ in range(dec_depth)])
        self.dec_norm = nn.LayerNorm(dec_dim)
        self.pred = nn.Linear(dec_dim, PH * PW)
        self.mask_ratio = mask_ratio
        nn.init.normal_(self.mask_token, std=0.02)

    @staticmethod
    def patchify(x):
        """[B,1,64,W] -> [B, R*C, PH*PW] row-major, matching the encoder's token order."""
        B, _, H, W = x.shape
        R, C = H // PH, W // PW
        return x.reshape(B, R, PH, C, PW).permute(0, 1, 3, 2, 4).reshape(B, R * C, PH * PW)

    @staticmethod
    def unpatchify(p, H, W):
        B = p.shape[0]
        R, C = H // PH, W // PW
        return p.reshape(B, R, C, PH, PW).permute(0, 1, 3, 2, 4).reshape(B, 1, H, W)

    def forward(self, x_in, x_clean):
        t, C = self.encoder.tokens(x_in)
        B, N, D = t.shape
        keep = int(N * (1 - self.mask_ratio))
        noise = torch.rand(B, N, device=t.device)
        order = noise.argsort(1)
        restore = order.argsort(1)
        vis_idx = order[:, :keep]
        vis = torch.gather(t, 1, vis_idx[..., None].expand(-1, -1, D))
        h = self.encoder.run(vis)

        d = self.enc_to_dec(h)
        full = torch.cat([d, self.mask_token.expand(B, N - keep, -1)], 1)
        full = torch.gather(full, 1, restore[..., None].expand(-1, -1, d.shape[-1]))
        full = full + sincos_2d(x_in.shape[2] // PH, C, d.shape[-1], t.device)[None]
        for b in self.dec:
            full = b(full)
        pred = self.pred(self.dec_norm(full)).float()  # B, N, PH*PW

        target = self.patchify(x_clean).float()
        err = ((pred - target) ** 2).mean(-1)  # B, N
        masked = torch.ones(B, N, device=t.device)
        masked.scatter_(1, vis_idx, 0.0)
        loss = (err * masked).sum() / masked.sum() + VIS_W * (err * (1 - masked)).sum() / (1 - masked).sum()
        return loss, pred, masked
