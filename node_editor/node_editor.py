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
from kivy.uix.widget import Widget

from nn_modules.code_names import *
from utility.custom_input.custom_input import CustomTextInput
from .property_form import PropertyForm
from .nl_form import NLForm
from .node_form import NodeForm

import nn_modules.nn_components


class NodeEditor(Popup):
    def __init__(self, **kwargs):
        super(NodeEditor, self).__init__()
        self.size_hint_x = 0.3
        self.scroll_view = ScrollView(size_hint=(1, 0.9))

        self.code_names = [INT_CODE,
                           STR_CODE,
                           FLOAT_CODE]

        self.node_type_list = {'Normal': NORM,
                               'Stacked': STACKED,
                               'Function': FUNCTION}
        self.node_type = self.node_type_list['Normal']
        self.key = 'Normal'

        self.n_in_links = NLForm(hint_text='Number of Inputs')
        self.n_out_links = NLForm(hint_text='Number of Outputs',
                                  nl_type='output')

        self.main_layout = BoxLayout(size_hint=(1, 1),
                                     orientation='vertical',
                                     spacing=4,
                                     padding=(2, 6, 2, 6))

        self.custom_title = GridLayout(size_hint=(1, 0.05),
                                       padding=4,
                                       cols=3,
                                       rows=1,
                                       spacing=2)

        self.main_sub_layout = GridLayout(size_hint=(1, None),
                                          cols=2,
                                          row_force_default=True,
                                          row_default_height=30,
                                          spacing=5)

        # self.node_link_type_chooser = Spinner(text='left',
        #                                       values=('left',
        #                                               'right',
        #                                               'top',
        #                                               'bottom'),
        #                                       size_hint_x=0.3)

        self.node_type_chooser = Spinner(text='Normal',
                                         values=('Normal',
                                                 'Stacked',
                                                 'Function'),
                                         size_hint_x=0.28)
        self.node_type_chooser.bind(text=self.change_node)

        self.add_custom_title()
        self.init_layouts()

        # self.node_template = {}
        self.screen_manager = kwargs.get('screen_manager')
        self.tab_manager = self.screen_manager.get_screen('scripting').children[-1].children[1]
        self.component_panel = kwargs.get('component_panel')

        self.auto_dismiss = False

    # def choose_node_type(self, obj, text):
    #     print(text)

    def add_custom_title(self):
        button = Button(text='X',
                        size_hint_x=0.1)
        button.bind(on_press=lambda obj: self.dismiss())

        self.custom_title.add_widget(CustomTextInput(size_hint_x=0.4,
                                                     size_hint_y=0.65,
                                                     max_length=100))
        # self.custom_title.add_widget(Label(size_hint_x=0.48))
        self.custom_title.add_widget(self.node_type_chooser)
        self.custom_title.add_widget(button)

        self.children[0].remove_widget(self.children[0].children[2])
        temp = self.children[0].children[1]
        self.children[0].remove_widget(self.children[0].children[1])
        self.children[0].remove_widget(self.children[0].children[-1])

        self.children[0].add_widget(self.custom_title)
        self.children[0].add_widget(temp)

    def add_main_sub_layout(self):
        self.main_sub_layout.bind(minimum_height=self.main_sub_layout.setter('height'))

        # # Number of inputs
        # n_inputs_layout = BoxLayout(size_hint=(0.8, 0.05),
        #                             spacing=6)
        # n_inputs = CustomTextInput(size_hint_x=0.7)
        # n_inputs.bind(text=lambda obj, value: setattr(self,
        #                                               'n_inputs',
        #                                               int(value)))
        #
        # # n_inputs_layout.add_widget(Label(text='n_inputs', size_hint_x=0.2))
        # n_inputs_layout.add_widget(n_inputs)
        # n_inputs_layout.add_widget(Button(text='position', size_hint_x=0.3))
        #
        # self.main_sub_layout.add_widget(Label(text='n_inputs', size_hint_x=0.2))
        # self.main_sub_layout.add_widget(n_inputs_layout)
        #
        # # Number of outputs
        # n_outputs_layout = BoxLayout(size_hint=(0.8, 0.05),
        #                              spacing=6)
        # n_outputs = CustomTextInput(size_hint_x=0.7)
        # n_outputs.bind(text=lambda obj, value: setattr(self,
        #                                                'n_outputs',
        #                                                int(value)))
        #
        # # n_outputs_layout.add_widget(Label(text='n_outputs', size_hint_x=0.2))
        # n_outputs_layout.add_widget(n_outputs)
        # n_outputs_layout.add_widget(Button(text='position', size_hint_x=0.3))
        #
        # self.main_sub_layout.add_widget(Label(text='n_outputs', size_hint_x=0.2))
        # self.main_sub_layout.add_widget(n_outputs_layout)

        labels_layout = GridLayout(size_hint=(1, 0.04),
                                   cols=2,
                                   row_force_default=True,
                                   row_default_height=30,
                                   spacing=5)

        labels_sub_layout = BoxLayout()
        labels_sub_layout.add_widget(Label(text='Property Name', size_hint_x=0.6))
        labels_sub_layout.add_widget(Label(text='Value', size_hint_x=0.2))
        labels_sub_layout.add_widget(Label(text='Datatype', size_hint_x=0.2))

        labels_layout.add_widget(Label(size_hint_x=0.1))
        labels_layout.add_widget(labels_sub_layout)

        self.scroll_view.add_widget(self.main_sub_layout)

        self.add_nn_links()
        self.main_layout.add_widget(labels_layout)
        self.main_layout.add_widget(self.scroll_view)

    def add_nn_links(self):
        sub_layout = BoxLayout(orientation='vertical',
                               size_hint=(1, 0.13),
                               spacing=6)

        labels_layout = BoxLayout(size_hint=(1, 0.4))
        # labels_layout.add_widget(Label(text='Link Type', size_hint_x=0.4))
        labels_layout.add_widget(Label(text='Number Of Links', size_hint_x=0.7))
        labels_layout.add_widget(Label(text='Position', size_hint_x=0.3))

        sub_layout.add_widget(labels_layout)

        sub_layout.add_widget(self.n_in_links)
        sub_layout.add_widget(self.n_out_links)

        self.main_layout.add_widget(sub_layout)

    def init_layouts(self):
        self.add_main_sub_layout()
        self.add_adding_button()
        self.add_create_node_button()

        self.children[0].add_widget(self.main_layout)

    def add_create_node_button(self):
        layout = BoxLayout(size_hint=(1, 0.05))
        create_node = Button(text='Create Node',
                             size_hint=(0.6, 1))
        create_node.bind(on_press=self.create_node)

        layout.add_widget(Label(size_hint=(0.4, 1)))
        layout.add_widget(create_node)
        self.main_layout.add_widget(layout)

    def add_adding_button(self):
        button = Button(text='+', size_hint=(0.1, 1))
        button.bind(on_press=self.add_property_form)
        self.main_sub_layout.add_widget(button)

    def change_node(self, obj, text):
        self.key = text
        self.clear_main_sub_layout()

    def clear_main_sub_layout(self):
        self.main_sub_layout.clear_widgets()
        self.add_adding_button()

    def add_property_form(self, obj):
        if self.key == 'Normal' or self.key == 'Function':
            form_type = PropertyForm()
        else:
            form_type = NodeForm()

        self.main_sub_layout.add_widget(form_type)

        self.add_adding_button()
        self.change_button_functionality(obj)

    def create_node(self, obj, nn_modules=None):
        import nn_modules
        properties = {}
        attributes = {}

        with open('nn_modules\\nn_nodes.json', 'r') as f:
            nodes = json.load(f)

        for i in range(0, len(self.main_sub_layout.children)):
            _property = self.main_sub_layout.children[i].property

            if type(_property) == dict and 'position' not in _property.keys():
                properties.update({_property['property_name']: [_property['dtype'],
                                                                str(_property['default_value'])]})

        # Add `node_type` property
        attributes.update({'node_type': self.node_type})
        attributes.update({'nl_input': self.n_in_links.property})
        attributes.update({'nl_output': self.n_out_links.property})

        node_name = self.custom_title.children[2].text

        if node_name != '':
            if node_name[0].islower():
                prefix = node_name[0].upper()
                node_name = prefix + node_name[1::]

            # nodes.update({node_name: properties})

            code_template = self.get_code_template(node_name)

            self.screen_manager.current = 'scripting'
            self.tab_manager.add_tab(func_name=node_name,
                                     _fkwargs={'text': code_template})

            tab = self.tab_manager.tab_list[-1]
            self.tab_manager.switch_to(tab)
            self.add_alg_file(node_name,
                              code_template)

            # with open('nn_modules\\nn_nodes.json', 'w') as f:
            #     json.dump(nodes, f, sort_keys=True, indent=4)

            attributes.update({'node_name': node_name})

            importlib.reload(nn_modules.nn_components)
            self.component_panel.update_panel()
            self.dismiss()

    # REMOVE COMPONENTS FROM THE COMPONENT PANEL THEN UPDATING IT

    @staticmethod
    def add_alg_file(node_name, code_template):
        with open('algorithms\\{0}.py'.format(node_name), 'w') as f:
            f.write(code_template)

    @staticmethod
    def get_code_template(node_name):
        with open('i_modules\\code_template.py', 'r') as f:
            lines = f.readlines()
            code_template = ''
            lines[0] = lines[0].format(node_name.lower())

            for line in lines:
                code_template = code_template + line

        return code_template

    def remove_property(self, obj):
        index = obj.parent.children.index(obj) - 1
        self.main_sub_layout.remove_widget(self.main_sub_layout.children[index])
        self.main_sub_layout.remove_widget(obj)

    def change_button_functionality(self, obj):
        obj.text = '-'
        obj.unbind(on_press=self.add_property_form)
        obj.bind(on_press=self.remove_property)
