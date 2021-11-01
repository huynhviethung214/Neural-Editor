from kivy.base import runTouchApp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scatterlayout import ScatterLayout, ScatterPlaneLayout
from kivy.uix.stencilview import StencilView
from test_node import layout
from kivy.app import App
from kivy.lang.builder import Builder


class Interface(StencilView, BoxLayout):
    def __init__(self, **kwargs):
        super(Interface, self).__init__()
        self.scatter_plane = ScatterPlaneLayout()
        self.size_hint = (1, 1)

        self.scatter_plane.add_widget(layout())
        self.scatter_plane.add_widget(layout())
        self.add_widget(self.scatter_plane)


class app(App):
    def build(self):
        return Builder.load_file('test_interface.kv')


if __name__ == '__main__':
    app().run()
