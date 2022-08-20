import json
from nn_modules.node import Node
from schematics.node_schematic import NodeSchematic


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
                # globals()[_name].schema = nodes[node_name]

                globals()[_name].name = node_name
                globals()[_name].algorithm = algo


generate_nn_nodes()
