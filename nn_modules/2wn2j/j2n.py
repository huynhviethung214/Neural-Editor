import json
from nn_modules.node import Node


def request_node(nodeName):
    with open('./nn_modules/nn_nodes.json', 'r') as f:
        schema = json.load(f)
        node = schema[nodeName]

        # `attributes`
        attributes = node['attributes']
        node_type = attributes['node_type']  # Can be 8 / 9 / 10 (See code_names.py)
        node_class = attributes['node_class']  # Can be any varieties of nodeName i.e `BatchNorm2D 0`
        nl_input = attributes['nl_input']
        nl_output = attributes['nl_output']

        # `sub_nodes`
        sub_nodes = node['sub_nodes']

        # `graphic_attributes`
        graphic_attributes = node['graphic_attributes']
        node_pos = graphic_attributes['node_pos']
        bcoord = graphic_attributes['bcoord']

        cmap = node['cmap']

        # `properties`
        properties = node['properties']
        layer = properties['layer']
