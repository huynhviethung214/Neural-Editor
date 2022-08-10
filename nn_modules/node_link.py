from kivy.graphics import Rectangle
from kivy.uix.widget import Widget


class NodeLink(Widget):
    def __init__(self, **kwargs):
        self.name = kwargs.get('name')

        super(NodeLink, self).__init__()
        self.size_hint = (None, None)
        self.size = (12, 12)

        self.gateType = kwargs.get('_type')  # Input is 1 and Output is 0
        self.node = kwargs.get('node')
        self.pos = kwargs.get('pos')
        self.connected = False

        self.c_pos = None
        self.t_pos = None
        self.target = None

        self.draw_widget()

    def index(self):
        return int(self.name.split(' ')[-1])

    def draw_widget(self):
        with self.canvas:
            Rectangle(pos=self.pos,
                      size=self.size)
