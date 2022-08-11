class InterfaceSchematic:
    def __init__(self):
        self.schema = {
            'nodes': {},
            'cmap': [],
            'touch_info': {
                'down': '',
                'up': ''
            }
        }

    # `nodes`
    def nodes_get(self, node_name: str):
        return self.schema['nodes'][node_name]

    def nodes_set(self, node_name: str, node_schema):
        self.schema['nodes'][node_name] = node_schema

    # `cmap`
    def cmap_get(self):
        return self.schema['cmap']

    def cmap_set(self, nodes_connection: [str, str]):
        self.schema['cmap'].append(nodes_connection)

    # `touch-info`
    def touch_info_get(self, key: str):
        return self.schema['touch_info'][key]

    def touch_info_set(self, key: str, value):
        self.schema['touch_info'][key] = value
