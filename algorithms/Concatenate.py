import torch
from torch.nn import Module


class Concat(Module):
    def __init__(self, dimension=0):
        super(Concat, self).__init__()
        self.dimension = dimension

    def forward(self, x1, x2):
        # print(self.dimension)
        return torch.cat((x1, x2),
                         self.dimension)


def algorithm(self):
    # print(self.properties)
    return Concat(dimension=self.properties['dimension'][1])
