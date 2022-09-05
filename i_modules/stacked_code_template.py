import torch
import numpy as np
from Net.Net import Net
from settings.config import configs
# IMPORT AS MANY MODULES AS YOU NEED


# `self` has `properties` attribute which contain `inputs` that you have been
# added in the `Node Editor`

def algorithm(self):
    # YOUR CODE GOES HERE
    # self.load_nodes()
    return Net(nodes=self.schema['sub_nodes'],
               interface=self.interface).to(configs['device']['id'])
