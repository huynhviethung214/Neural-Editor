from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout

from kivy.garden.matplotlib import FigureCanvasKivyAgg

import numpy as np
from matplotlib import pyplot as plt


class Graphs(GridLayout):
    def __init__(self, **kwargs):
        super(Graphs, self).__init__()
        self.graphs = kwargs.get('graphs')
        self.add_graphs()

    def add_graphs(self):
        n_graphs = len(self.graphs.keys())

        if n_graphs % 2 == 0:
            self.rows = self.cols = n_graphs
        else:
            self.rows = self.cols = n_graphs + 1

        for graph_name in self.graphs.keys():
            xlabel = self.graphs[graph_name]['xlabel']

            ylabel = self.graphs[graph_name]['ylabel']

            plt.figure()
            epochs = self.graphs[graph_name]['epochs']
            plt.plot(range(len(self.graphs[graph_name]['losses'])),
                     self.graphs[graph_name]['losses'])
            plt.xticks(np.arange(0,
                                 epochs,
                                 [1.0 if epochs <= 20 else int((epochs * 5.0) / 20.0)][0]))
            plt.xlabel(xlabel)
            plt.ylabel(ylabel)
            plt.grid(True, color='lightgray')

            layout = BoxLayout(orientation='vertical')
            layout.add_widget(Label(text=graph_name,
                                    size_hint_y=0.05))
            layout.add_widget(FigureCanvasKivyAgg(plt.gcf()))
            self.add_widget(layout)
