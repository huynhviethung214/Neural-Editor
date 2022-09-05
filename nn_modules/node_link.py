from kivy.graphics import Rectangle
from kivy.uix.widget import Widget

from schematics.node_link_schematic import NodeLinkSchematic


class NodeLink(Widget, NodeLinkSchematic):
    def __init__(self, _type=None, node=None, name=None, **kwargs):
        self.name = name

        super(NodeLink, self).__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (12, 12)

        self.schema_set('gate_type', _type)
        # self.schema_set('rec_pos', kwargs.get('pos'))
        self.schema_set('c_pos', kwargs.get('pos'))
        # self.pos = kwargs.get('pos')

        # self.gateType = kwargs.get('_type')  # Input is 1 and Output is 0
        self.node = node

        # self.node = kwargs.get('node')
        # self.pos = kwargs.get('pos')
        # self.connected = False

        # self.c_pos = None
        # self.t_pos = None
        # self.target = None

        self.draw_widget()

    def to_scatter_plane(self, scatter_plane):
        return scatter_plane.to_widget(*self.to_window(*self.to_local(*self.pos)))

    def index(self):
        return int(self.name.split(' ')[-1])

    def draw_widget(self):
        with self.canvas:
            Rectangle(pos=self.pos,
                      size=self.size)
