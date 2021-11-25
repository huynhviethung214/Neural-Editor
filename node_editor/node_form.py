import json

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner

from nn_modules.code_names import *
from utility.custom_input.custom_input import CustomTextInput


class NodeForm(BoxLayout):
    def __init__(self, **kwargs):
        super(NodeForm, self).__init__()
        self.size_hint = (0.9, 1)
        self.spacing = 4
        self.function = None

        with open('nn_modules\\nn_nodes.json', 'r') as f:
            nodes = json.load(f)
            node_names = [node_name for node_name in nodes.keys()]
            self.datatype_list = Spinner(values=tuple(node_names),
                                         size_hint=(0.2, 1),
                                         text=node_names[0],
                                         sync_height=True)
            self.datatype_list.bind(text=self.change_node)

            self.add_widget(self.datatype_list)

    # Change `self.function` accordingly to the chosen node
    def change_node(self, obj, text):
        pass
