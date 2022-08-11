import json
from nn_modules.code_names import LAYER_CODE


def post_node(attributes, properties):
    node_name = attributes['node_name']

    with open('nn_modules\\nn_nodes.json', 'r') as fr:
        nodes = json.load(fr)

    with open('nn_modules\\nn_nodes.json', 'w') as fw:
        schema = {
            'attributes': {
                'node_type': attributes['node_type'],
                'node_class': attributes['node_name'],
                'nl_input': attributes['nl_input'],
                'nl_output': attributes['nl_output'],
                'layer': 'Hidden Layer'
            },
            'sub_nodes': {},
            'graphic_attributes': {
                'node_pos': (0, 0),
                'beziers_coord': []
            },
            'cmap': [],
            'properties': properties,
            'script': f'algorithms/{node_name}.py'
        }

        nodes.update({attributes['node_name']: schema})
        json.dump(nodes, fw, sort_keys=True, indent=4)
