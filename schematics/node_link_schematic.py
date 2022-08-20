class NodeLinkSchematic:
    def __init__(self):
        self.schema = {
            'target': None,
            'gate_type': 0,
            'name': '',
            'connected': False,
            'target_pos': [0, 0],
            'c_pos': [0, 0]
        }

    def apply_schematic(self, schema):
        self.schema = schema

    def schema_get(self, key: str):
        return self.schema[key]

    def schema_set(self, key: str, value):
        self.schema[key] = value
