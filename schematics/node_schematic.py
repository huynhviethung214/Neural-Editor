class NodeSchematic:
    def __init__(self, schema):
        self.schema = schema

    # `attributes`
    def attributes_get(self, key: str):
        return self.schema['attributes'][key]

    def attributes_set(self, key: str, value):
        self.schema['attributes'][key] = value

    # `nl_input`
    def nl_input_get(self, key: str):
        return self.schema['attributes']['nl_input'][key]

    def nl_input_set(self, key: str, value):
        self.schema['attributes']['nl_input'][key] = value

    # `nl_output`
    def nl_output_get(self, key: str):
        return self.schema['attributes']['nl_output'][key]

    def nl_output_set(self, key: str, value):
        self.schema['attributes']['nl_output'][key] = value

    # `layer`
    def layer_get(self):
        return self.schema['attributes']['layer'][1]

    def layer_set(self, value: str):
        self.schema['attributes']['layer'][1] = value

    # `sub_nodes`
    def sub_nodes_get(self, sub_node_name: str):
        return self.schema['sub_nodes'][sub_node_name]

    def sub_nodes_set(self, sub_node_name: str, schema: {}):
        self.schema['sub_nodes'][sub_node_name] = schema

    # `graphic_attributes`
    def graphic_attributes_get(self, value: str):
        return self.schema['graphic_attributes'][value]

    def beziers_coord_set(self, index: int, value: [float, float]):
        self.schema['graphic_attributes']['beziers_coord'][index] = value

    def node_pos_set(self, value: [float, float]):
        self.schema['graphic_attributes']['node_pos'] = value

    # `Connectivity map for `sub_nodes``
    def cmap_get(self):
        return self.schema['cmap']

    def cmap_set(self, nodes_connection: [str, str]):
        self.schema['cmap'].append(nodes_connection)

    # `properties`
    def properties_get(self, key: str):
        return self.schema['properties'][key][0], self.schema['properties'][key][1]

    def properties_set(self, key: str, _type: int, value):
        self.schema['properties'][key][0] = _type
        self.schema['properties'][key][1] = value

    # `script`
    def script_get(self):
        return self.schema['script']

    def script_set(self, value):
        self.schema['script'] = value
