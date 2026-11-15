"""CRNN: VGG-style CNN -> 2-layer BiLSTM -> linear (CTC).

Input  [B, 1, 64, W] (ink = 1). Output log-probs [T, B, C] with T = W / 4.
About 8M parameters with the defaults.
"""
import torch
import torch.nn as nn


def block(cin, cout, pool):
    layers = [nn.Conv2d(cin, cout, 3, padding=1, bias=False), nn.BatchNorm2d(cout), nn.ReLU(inplace=True)]
    if pool is not None:
        layers.append(nn.MaxPool2d(pool))
    return layers


class CRNN(nn.Module):
    def __init__(self, n_classes, height=64, hidden=256, dropout=0.25):
        super().__init__()
        assert height == 64
        self.cnn = nn.Sequential(
            *block(1, 64, (2, 2)),        # 32 x W/2
            *block(64, 128, (2, 2)),      # 16 x W/4
            *block(128, 256, None),
            *block(256, 256, (2, 1)),     # 8 x W/4
            *block(256, 384, None),
            *block(384, 384, (2, 1)),     # 4 x W/4
            *block(384, 384, (4, 1)),     # 1 x W/4
            nn.Dropout2d(dropout * 0.5),
        )
        self.rnn = nn.LSTM(384, hidden, num_layers=2, bidirectional=True, dropout=dropout, batch_first=False)
        self.drop = nn.Dropout(dropout)
        self.head = nn.Linear(2 * hidden, n_classes)
        self.stride = 4

    def features(self, x, widths=None):  # widths unused: kept for a common interface
        """[B, D, T] sequence features before the recurrent layers (used for invariance scores)."""
        f = self.cnn(x)  # B, 384, 1, T
        return f.squeeze(2)

    def forward(self, x, widths=None):
        f = self.features(x).permute(2, 0, 1)  # T, B, D
        h, _ = self.rnn(f)
        return self.head(self.drop(h)).float().log_softmax(-1)  # T, B, C

    def out_lengths(self, widths):
        return torch.div(widths, self.stride, rounding_mode="floor").clamp(min=1)

    def load_encoder(self, path):
        """Load a pretrained CNN (keys "cnn.*", e.g. from ConvMAE); the BiLSTM and head stay fresh."""
        sd = torch.load(path, map_location="cpu")
        sd = {k: v for k, v in sd.items() if k.startswith("cnn.")}
        return self.load_state_dict(sd, strict=False)

    def set_encoder_trainable(self, flag):
        for p in self.cnn.parameters():
            p.requires_grad_(flag)
