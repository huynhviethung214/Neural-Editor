# IMPORT AS MANY MODULES AS YOU NEED
import torch
import numpy as np
from torch.nn import Module


class Div(Module):
    def forward(self, x):
        return x, x


# `self` has `properties` attribute which contain `inputs` that you have been
# added in the `Node Editor` (Add [1] at the end of self.properties[`prop's name`]
# to retrieve the property's value)

def algorithm(self):
    # YOUR CODE GOES HERE
    return Div()