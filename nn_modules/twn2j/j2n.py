import json
from nn_modules.node import Node


def request_node(node_name: str):
    with open('./nn_modules/nn_nodes.json', 'r') as f:
        schema = json.load(f)
        node = schema[node_name]

        # `attributes`
        attributes = node['attributes']
        node_type = attributes['node_type']  # Can be 8 / 9 / 10 (See code_names.py)
        node_class = attributes['node_class']  # Can be any varieties of `node_name` i.e `BatchNorm2D, Flatten, ...`
        nl_input = attributes['nl_input']
        nl_output = attributes['nl_output']

        # `sub_nodes`
        sub_nodes = node['sub_nodes']

        # `graphic_attributes`
        graphic_attributes = node['graphic_attributes']
        node_pos = graphic_attributes['node_pos']
        beziers_coord = graphic_attributes['beziers_coord']  # Info for rendering beziers if
                                                             # the number of `sub_nodes` > 0

        # Connectivity map for `sub_nodes`
        cmap = node['cmap']

        # `properties`
        properties = node['properties']
        layer = properties['layer']

        # `script`
        script = node['script']
