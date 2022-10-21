from kivy.graphics import Rectangle
from kivy.uix.widget import Widget

from schematics.node_link_schematic import NodeLinkSchematic
from utility.utils import round_pos


class NodeLink(Widget, NodeLinkSchematic):
    def __init__(self, _type=None, node=None, name=None, **kwargs):
        self.name = name

        super(NodeLink, self).__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (12, 12)

        self.schema_set('gate_type', _type)
        # self.schema_set('rec_pos', kwargs.get('pos'))
        # self.schema_set('c_pos', kwargs.get('pos'))
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

    def unbind(self):
        if self.schema_get('target'):
            target = self.node.interface.node_links[self.schema_get('target')]
            self.node.interface.remove_bezier(
                self.node.interface.get_bezier(self, target)
            )

            target.schema_set('target', None)
            target.schema_set('connected', False)

            self.schema_set('target', None)
            self.schema_set('connected', False)

    def get_center_position(self, scatter_plane):
        pos = list(self.to_scatter_plane(scatter_plane))
        pos[0] += self.width / 2
        pos[1] += self.height / 2
        pos = round_pos(pos)

        return pos

    def to_scatter_plane(self, scatter_plane):
        # to_interface = scatter_plane.parent.to_widget(*self.to_window(*self.pos))
        # return scatter_plane.to_local(*to_interface)
        return scatter_plane.to_widget(*self.to_window(*self.pos))

    def index(self):
        return int(self.name.split(' ')[-1])

    def draw_widget(self):
        with self.canvas:
            Rectangle(pos=self.pos,
                      size=self.size)
