import torch
from torch.nn import Module


class _flatten(Module):
    def forward(self, x):
        # print(x.size(0))
        try:
            # print(x)
            # return x.view(x.size(0), -1)
            return torch.flatten(x, start_dim=0)
            # return torch.reshape(x, (x.size(0),))
        except RuntimeError:
            pass


def algorithm(self):
    return _flatten()
