import json
import importlib

from nn_modules.node import Node
# from nn_modules.base_node import BaseNode

from i_modules.interface.interface import Interface
# from torch.nn import ReLU, BatchNorm2d, Conv2d, MaxPool2d, Linear, Sequential


def generate_nn_nodes():
    with open('nn_modules\\nn_nodes.json', 'r') as f:
        nodes = json.load(f)

        for node_name in nodes.keys():
            _name = node_name + 'Node'

            if _name not in globals():
                module = __import__(f'algorithms.{node_name}',
                                    fromlist=['algorithm'])
                algo = getattr(module, 'algorithm')

                globals()[_name] = type(_name,
                                        (Node,),
                                        {})

                globals()[_name].node_template = nodes[node_name]
                globals()[_name].name = node_name
                globals()[_name].node_type = nodes[node_name]['node_type']
                globals()[_name].algorithm = algo


generate_nn_nodes()
