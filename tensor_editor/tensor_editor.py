import importlib
import json

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView

# import nn_modules
from kivy.uix.spinner import Spinner

from nn_modules.code_names import *
from utility.custom_input.custom_input import CustomTextInput


class NodeEditor(Popup):
    def __init__(self, **kwargs):
        super(NodeEditor, self).__init__()
        self.size_hint_x = 0.2
        self.auto_dismiss = False

        self.add_custom_title()

    def add_custom_title(self):
        button = Button(text='X',
                        size_hint_x=0.1)
        button.bind(on_press=lambda obj: self.dismiss())

        self.custom_title.add_widget(CustomTextInput(size_hint_x=0.4,
                                                     size_hint_y=0.65))
        # self.custom_title.add_widget(Label(size_hint_x=0.48))
        self.custom_title.add_widget(self.node_type_chooser)
        self.custom_title.add_widget(button)

        self.children[0].remove_widget(self.children[0].children[2])
        temp = self.children[0].children[1]
        self.children[0].remove_widget(self.children[0].children[1])
        self.children[0].remove_widget(self.children[0].children[-1])

        self.children[0].add_widget(self.custom_title)
        self.children[0].add_widget(temp)
