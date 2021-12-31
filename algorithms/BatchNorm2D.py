import torch
import numpy as np
from torch.nn import BatchNorm2d
from utility.utils import map_properties


@map_properties
def algorithm(self):
    return BatchNorm2d