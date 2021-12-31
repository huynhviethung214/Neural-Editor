import torch
import numpy as np
from torch.nn import ReLU
from utility.utils import map_properties


@map_properties
def algorithm(self):
    # YOUR CODE GOES HERE
    return ReLU