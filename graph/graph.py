import numpy as np

from kivy.app import App
from kivy.graphics import Color
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics.vertex_instructions import Line


class Graph(GridLayout):
    def __init__(self, **kwargs):
        super(Graph, self).__init__()
        self.cols = 2
        self.rows = 2

        self.interface = kwargs.get('interface')
        self.scale_factor = 10
        # print(kwargs)
        # self.data_points = kwargs.get('data_points')
        self.data_points = [100, 100, 200, 200, 300, 300]
        # self.draw_graph()

        self.graph = GridLayout(size_hint=(0.92, 0.9))
        self.y_axis = GridLayout(cols=1,
                                 size_hint=(0.08, 0.9))
        self.x_axis = GridLayout(rows=1,
                                 size_hint=(0.92, 0.1))

        self.origin = BoxLayout(size_hint=(0.08, 0.1))
        self.origin.add_widget(Label(text='Origin',
                                     halign='center',
                                     valign='center',
                                     size_hint=(1, 1)))

        self.add_widget(self.y_axis)
        self.add_widget(self.graph)
        self.add_widget(self.origin)
        self.add_widget(self.x_axis)

    def shift_data_points_to_local(self):
        new_dp = []

        for i in range(0, len(self.data_points), 2):
            new_x = self.data_points[i] + self.graph.pos[0]
            new_y = self.data_points[i + 1] + self.graph.pos[1]
            new_dp.append(new_x)
            new_dp.append(new_y)

        self.data_points = new_dp

    def draw_axes(self):
        x = self.graph.pos[0]
        y = self.graph.pos[1]

        with self.graph.canvas:
            Color(0, 0, 1, 1)
            # y-axis
            Line(points=[x, y, x, y + (self.height - 120)], width=1)
            # x-axis
            Line(points=[x, y, x + (self.width - 200), y], width=1)

    def draw_graph(self):
        # self.graph.canvas.clear()
        self.draw_axes()
        self.shift_data_points_to_local()
        # self.scale_dp()

        with self.graph.canvas:
            Color(1, 0, 0, 1)
            Line(points=self.data_points, width=1)

    # def scale_dp(self):
    #     for i in range(len(self.data_points)):
    #         self.data_points[i] *= self.scale_factor
    #         self.data_points[i] += self.offset[0]
    #         self.data_points[i + 1] += self.offset[1]


class app(App):
    def build(self):
        return Graph()


if __name__ == '__main__':
    app().run()
