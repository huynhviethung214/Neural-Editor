import torch
import numpy as np
from torch.nn import MaxPool2d
from utility.utils import map_properties


@map_properties
def algorithm(self):
    # YOUR CODE GOES HERE
    return MaxPool2d