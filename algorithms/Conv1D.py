from torch.nn import Conv1d
from utility.utils import map_properties


@map_properties
def algorithm(self):
    return Conv1d
