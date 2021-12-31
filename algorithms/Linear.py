from torch.nn import Linear
from utility.utils import map_properties


@map_properties
def algorithm(self):
    return Linear
