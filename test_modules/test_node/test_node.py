from kivy.uix.behaviors import DragBehavior, ButtonBehavior
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.scatterlayout import ScatterLayout
from kivy.app import runTouchApp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from utility.utils import get_obj

# NL
#   pos0 = current pos
#   pos1 = current mouse move pos
#   otd => set pos0


class NL(ButtonBehavior, Widget):
    def __init__(self, **kwargs):
        super(NL, self).__init__()
        self.connected = 0 # 0 = NOT CONNECTED, 1 = CONNECTED
        self.nl_type = 0 # 0 = OUTPUT, 1 = INPUT
        self.connected_node = None
        self.interface = kwargs.get('interface')

        self.pos0 = None
        self.pos1 = None

    def to_interface(self, pos):
        return self.interface.to_widget(*pos)

    # def on_touch_down(self, touch):
    #     if self.collide_point(*touch.pos):
    #         if self.nl_type == 0 and self.connected:
    #             self.connected_node.output_nl.pos1 = self.to_interface(touch.pos)
    #
    #         return True

    def on_touch_move(self, touch):
        if self.collide_point(*touch.pos):
            if self.nl_type == 0 and self.connected:
                # self.connected_node.output_nl.pos1 = self.to_interface(touch.pos)
                print(self.to_interface(touch.pos))

            return True


class Node(BoxLayout):
    def __init__(self, **kwargs):
        super(Node, self).__init__()
        self.padding = 10
        self.spacing = 5
        self.size_hint = (1, 1)
        self.orientation = 'vertical'

        self.sub_layout = BoxLayout(orientation='horizontal',
                                    spacing=4)

        self.nl1_layout = BoxLayout(size_hint=(0.1, 1),
                                    orientation='vertical',
                                    padding=(0, 20, 0, 20),
                                    spacing=60)
        self.nl1_layout.add_widget(NL())
        self.nl1_layout.add_widget(NL())
        self.nl1_layout.add_widget(NL())

        self.nl2_layout = BoxLayout(size_hint=(0.1, 1),
                                    orientation='vertical',
                                    padding=(0, 20, 0, 20),
                                    spacing=60)
        self.nl2_layout.add_widget(NL())
        self.nl2_layout.add_widget(NL())
        self.nl2_layout.add_widget(NL())

        self.nl3_layout = BoxLayout(orientation='horizontal',
                                    size_hint=(1, 0.1),
                                    spacing=60,
                                    padding=(40, 0, 40, 0))
        self.nl3_layout.add_widget(NL())
        self.nl3_layout.add_widget(NL())
        self.nl3_layout.add_widget(NL())

        self.nl4_layout = BoxLayout(orientation='horizontal',
                                    size_hint=(1, 0.1),
                                    spacing=60,
                                    padding=(40, 0, 40, 0))
        self.nl4_layout.add_widget(NL())
        self.nl4_layout.add_widget(NL())
        self.nl4_layout.add_widget(NL())

        self.content_layout = BoxLayout(orientation='vertical',
                                        spacing=6)
        self.content_layout.add_widget(NL())
        self.content_layout.add_widget(NL())
        self.content_layout.add_widget(NL())

        self.sub_layout.add_widget(self.nl1_layout)
        self.sub_layout.add_widget(self.content_layout)
        self.sub_layout.add_widget(self.nl2_layout)

        self.add_widget(self.nl3_layout)
        self.add_widget(self.sub_layout)
        self.add_widget(self.nl4_layout)

    def test(self, obj):
        print(obj)


class layout(FloatLayout):
    def __init__(self, **kwargs):
        super(layout, self).__init__()
        self.scatter_layout = ScatterLayout()
        self.size = (300, 300)

        self.scatter_layout.add_widget(Node())

        self.add_widget(self.scatter_layout)
