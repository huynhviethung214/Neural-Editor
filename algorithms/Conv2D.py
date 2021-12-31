import torch
import numpy as np
from torch.nn import Conv2d
from utility.utils import map_properties


@map_properties
def algorithm(self):
    return Conv2d