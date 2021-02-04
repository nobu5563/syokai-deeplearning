import numpy as np
import torch
import torch.nn as nn

class ScaledDotProductAttention(nn.Module):
    def __init__(self, d_k, device='cpu'):
        super().__init__()
        self.device = device
        self.scaler = np.sqrt(d_k)

    def forward(self, q, k, v, mask=None):
        score = torch.einsum('ijk,ilk->ijl', (q, k)) / self.scaler