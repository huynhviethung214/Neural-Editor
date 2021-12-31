from torch.nn import Conv3d
from utility.utils import map_properties


@map_properties
def algorithm(self):
    return Conv3d
