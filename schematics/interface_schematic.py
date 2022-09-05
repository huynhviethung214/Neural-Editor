class InterfaceSchematic:
    def __init__(self):
        self.schema = {
            'nodes': {},
            'cmap': [],
            'hvfs': None,
            'touch_info': {
                'down_node_link': None,
                'down_pos': [0, 0],
                'selected': None
            },
            'beziers_coord': [],
            'train_log': {}
        }

    # `nodes`
    def nodes_get(self, node_name: str):
        return self.schema['nodes'][node_name]

    def nodes_set(self, node_name: str, node_schema):
        self.schema['nodes'][node_name] = node_schema

    # `beziers_coord`
    def beziers_coord_get(self):
        return self.schema['beziers_coord']

    def beziers_coord_set(self, value: [float, float]):
        self.schema['beziers_coord'].append(value)

    # `cmap`
    def cmap_get(self):
        return self.schema['cmap']

    def cmap_set(self, nodes_connection: [str, str]):
        self.schema['cmap'].append(nodes_connection)

    # `hvfs`
    def hvfs_get(self):
        return self.schema['hvfs']

    def hvfs_set(self, hvfs):
        self.schema['hvfs'] = hvfs

    # `touch-info`
    def touch_info_get(self, key: str):
        return self.schema['touch_info'][key]

    def touch_info_set(self, key: str, value):
        self.schema['touch_info'][key] = value
