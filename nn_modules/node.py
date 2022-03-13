import copy
import json
import os
import kivy

from os.path import abspath
from kivy.base import runTouchApp
from kivy.event import EventDispatcher
from kivy.uix.scatterlayout import ScatterLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.spinner import Spinner
from kivy.uix.treeview import TreeView, TreeViewLabel, TreeViewNode
from kivy.uix.widget import Widget
from kivy.graphics import Line, Rectangle
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from functools import partial

from utility.rightclick_toolbar.rightclick_toolbar import RightClickMenu
from utility.utils import get_obj, draw_beziers, formatting_rels
from utility.custom_input.custom_input import CustomTextInput
from nn_modules.code_names import *

kivy.require('2.0.0')


class TreeViewLayout(BoxLayout, TreeViewNode):
    pass


class StateEvent(EventDispatcher):
    def __init__(self, state, **kwargs):
        self.register_event_type('on_state')
        super(StateEvent, self).__init__()
        self._state = state
        # self.function = kwargs.get('callback')

    def on_state(self, state):
        pass

    def set_state(self, new_state):
        self.dispatch('on_state', new_state)
        self._state = new_state


class NodeName(Label):
    def __init__(self, **kwargs):
        super(NodeName, self).__init__(**kwargs)


class NodeLink(Widget):
    ctd_state = {}

    def __init__(self, spawn_position, _type, node, name, **kwargs):
        self.name = name

        super(NodeLink, self).__init__()
        self.size_hint = (None, None)
        self.size = (12, 12)
        self.pos = spawn_position
        self.link_type = _type  # Input is 1 and Output is 0

        # self.callback = self._callback
        self.connected = False
        self.node = node
        # self.b_node = None
        # self.u_node = None

        # print(self.link_type)

        # self.input_bezier = None
        # self.output_bezier = None

        self.c_pos = None
        self.t_pos = None
        self.target = None

        self.draw_widget()

    # Dummy function
    # def _callback(self):
    #     return

    def index(self):
        return int(self.name.split(' ')[-1])

    def draw_widget(self):
        with self.canvas:
            Rectangle(pos=self.pos,
                      size=self.size)

    def __str__(self):
        return self.name


class CustomSpinnerInput(BoxLayout):
    def __init__(self, c_height=None, default_halign='center', **kwargs):
        super(CustomSpinnerInput, self).__init__()
        self.size_hint = (1, 1)
        self.height = c_height
        self.spacing = 20
        self.height = 25

        self.label = Label(text=kwargs.get('property_name'),
                           halign=default_halign,
                           valign='middle',
                           width=100,
                           font_size=14,
                           text_size=(100, 35),
                           size_hint=(0.4, 1),
                           max_lines=1,
                           shorten=True,
                           shorten_from='right')
        self.input = Spinner(text='False',
                             values=('True', 'False'),
                             size_hint=(0.6, 1),
                             sync_height=True)
        self.add_widget(self.label)
        self.add_widget(self.input)


class CustomValueInput(BoxLayout):
    def __init__(self, default_halign='center', **kwargs):
        super(CustomValueInput, self).__init__()
        self.size_hint = (1, 1)
        self.spacing = 20
        self.height = 25

        self.label = Label(text=kwargs.get('name'),
                           halign=default_halign,
                           valign='middle',
                           width=100,
                           font_size=14,
                           text_size=(100, 35),
                           size_hint=(0.4, 1),
                           max_lines=1,
                           shorten=True,
                           shorten_from='right')
        self.input = CustomTextInput(font_size=12,
                                     width=90,
                                     size_hint=(0.6, 1),
                                     max_length=30)

        self.add_widget(self.label)
        self.add_widget(self.input)


class KernelInput(BoxLayout):
    def __init__(self, **kwargs):
        super(KernelInput, self).__init__()
        self.default_size = kwargs.get('default_size')
        self.size_hint = (0.6, 1)
        self.spacing = 4
        self.height = 25

        self.m = CustomTextInput(text=str(self.default_size[0]),
                                 font_size=12)
        self.n = CustomTextInput(text=str(self.default_size[1]),
                                 font_size=12)

        self.add_widget(self.m)
        self.add_widget(Label(text='x',
                              size_hint_x=0.2))
        self.add_widget(self.n)


class Node(ScatterLayout):
    c_height = 25
    c_padding = 5
    c_spacing = 5

    n_layer = 0
    b_node = None

    # m_list = []
    # nodes_name = []
    in_list = {}

    def __init__(self, **kwargs):
        super(Node, self).__init__()
        self.layout = AnchorLayout(anchor_x='center',
                                   anchor_y='center')
        self.layout.padding = (4, 4, 4, 4)
        # self.rgba = (1, 1, 1, 1)

        self.sub_layout = GridLayout()
        self.sub_layout.cols = 1
        self.sub_layout.rows = 1
        # self.sub_layout.row_force_default = True
        # self.sub_layout.row_default_height = 25

        self.do_scale = False
        self.do_rotation = False
        self.width = 240

        # self.beziers = {'input': None,
        #                 'output': None}

        self.pos = kwargs.get('spawn_position')
        self.widget_height = 0
        self.c_nav = None

        self.code2pos = {
            LEFT_CODE: 'left',
            RIGHT_CODE: 'right',
            TOP_CODE: 'top',
            BOTTOM_CODE: 'bottom'
        }
        self.string_pos = {}

        self.types = ('Input Layer',
                      'Hidden Layer',
                      'Output Layer')
        self.c_type = self.types[1]

        self.type = NORM
        self.is_loaded = False

        self.properties = {}
        self.objs = []
        self.connected_nodes = []

        self.inputs = []
        self.outputs = []

        self.code_names = [INT_CODE, STR_CODE, FLOAT_CODE, OBJ_CODE]

        self.interface = kwargs.get('interface')
        self.interface_template = type(self.interface)()
        self.add_components()
        self.add_ib()

        self.funcs = {
            'De-grouping Node(s)': self.degrouping_nodes
        }

        # Combinding components and add event listener/handler
        self.combine()
        self.bind(on_touch_down=self.open_rightclick_menu)

    # In the future version `node_link` will be changed to `node_gate`
    def node_links(self, link_type: str):
        node_links = []

        for children in self.children[0].children:
            if type(children) == NodeLink and link_type in children.name:
                node_links.append(children)

        return node_links

    @staticmethod
    def get_algorithm(node_class):
        module = __import__(f'algorithms.{node_class}',
                            fromlist=['algorithm'])
        algo = getattr(module, 'algorithm')

        return algo

    def is_connected(self):
        c = 0
        node_links = copy.copy(self.outputs)
        node_links.extend(self.inputs)

        for node_link in node_links:
            if not node_link.target:
                c += 1

        if c == len(self.outputs) + len(self.inputs):
            return True
        return False

    @staticmethod
    def get_degrouped_node_class(node_class):
        module = __import__('nn_modules.nn_nodes',
                            fromlist=[node_class + 'Node'])
        return getattr(module, node_class + 'Node')

    def degrouping_nodes(self):
        if self.type == STACKED and self.is_connected():
            with open('./nn_modules/nn_nodes.json', 'r') as f:
                node_templates = json.load(f)

                hierarchy = get_obj(self.interface, 'Hierarchy')
                for hierarchy_node in hierarchy.iterate_all_nodes():
                    if hierarchy_node.text == self.name:
                        hierarchy.remove_node(hierarchy_node)
                        break

                for node_name in self.properties.keys():
                    try:
                        node_class = self.properties[node_name]['node_class']

                        # Node's template format
                        template = {
                            'pos': self.properties[node_name]['pos'],
                            'properties': {
                                'nl_input': node_templates[node_class]['nl_input'],
                                'nl_output': node_templates[node_class]['nl_output'],
                                'node_type': NORM,
                                'Layer': self.properties[node_name]['properties']['Layer']
                            }
                        }

                        # print(template)

                        for property_name in self.properties[node_name]['properties']:
                            template['properties'].update({
                                property_name: self.properties[node_name]['properties'][property_name]
                            })
                        # template['properties'].update({
                        #                                'Layer': self.properties[node_name]['properties']['Layer']})

                        # Initialize Node's properties
                        node = self.get_degrouped_node_class(node_class)
                        node.node_template = template['properties']
                        node.type = NORM
                        node.node_class = node_class
                        node.algorithm = self.get_algorithm(node_class)
                        node.name = node_name

                        self.interface._node = node
                        self.interface.template['model'].update({node_name: template})

                        node = self.interface.add_node2interface(
                            node_name=node_name,
                            spawn_position=self.properties[node_name]['pos']
                        )
                        node.c_type = \
                            node.drop_butt.text = \
                            self.properties[node_name]['properties']['Layer'][1]

                    except TypeError:
                        pass
                        # if 'Layer' in node_name:
                        #     self.set_type(None, self.properties['Layer'][1])

                draw_beziers(self.node_template,
                             self.interface)
                # print(self.interface.rels)
                self.interface.remove_node(self)
        else:
            print('[DEBUG]: Node is being connected to other Node(s). '
                  'Please disconnected them before de-grouping')

    def open_rightclick_menu(self, obj, touch):
        overlay = get_obj(self.interface, 'Overlay')

        if touch.button == 'right' and self.collide_point(*touch.pos):
            overlay.clear_menu()
            overlay.open_menu(menu_obj=RightClickMenu(funcs=self.funcs,
                                                      button_width=140,
                                                      pos=overlay.to_overlay_coord(touch, self)))

    def num_nl(self, nl_type=1):
        count = 0

        for children in self.children:
            if type(children) == NodeLink and children.c_type == nl_type:
                count += 1

        return count

    def add_node_links(self):
        self._add_node_links(self.node_template['nl_input']['n_links'],
                             self.node_template['nl_input']['position'],
                             'nl_input')

        self._add_node_links(self.node_template['nl_output']['n_links'],
                             self.node_template['nl_output']['position'],
                             'nl_output')

    def delete_node(self, obj):
        self.interface.remove_node(self)
        self.overlay.remove_widget(self.right_click_toolbar)

        for key in self.beziers.keys():
            if self.beziers[key]:
                try:
                    self.interface.clear_canvas()
                    Node.n_layer -= 1

                except ValueError:
                    pass

    def algorithm(self):
        pass

    def add_components(self):
        self.add_id()
        self.add_drop_down_list()

        if self.node_template['node_type'] == STACKED:
            self.add_stacked_nodes()
            self.type = STACKED
        else:
            self.sub_layout.row_force_default = True
            self.sub_layout.row_default_height = 25

            for key in self.node_template.keys():
                if key != 'node_type' and 'nl' not in key:
                    if self.node_template[key][0] in self.code_names:
                        self.add_val_input(name=key,
                                           _type=self.node_template[key][0],
                                           default_val=self.node_template[key][1])

                    elif self.node_template[key][0] == BOOL_CODE:
                        self.add_list_data(name=key,
                                           datas=[True, False],
                                           _type=BOOL_CODE)

                    elif self.node_template[key][0] == MATRIX_CODE:
                        self.add_kernel_input(name=key,
                                              default_size=(2, 2),
                                              _type=MATRIX_CODE)

    def _add_node_links(self, n_links, position, key):
        pos = self.code2pos[position]

        if n_links == 1:
            if 'output' in key:
                out1 = self.add_output_node(pos + '-middle')
                self.outputs.append(out1)
            else:
                in1 = self.add_input_node(pos + '-middle')
                self.inputs.append(in1)

        elif n_links == 2:
            if 'output' in key:
                out1 = self.add_output_node(pos=pos + '-top')
                out2 = self.add_output_node(pos + '-bottom',
                                            name='Output 1')
                self.outputs.append(out1)
                self.outputs.append(out2)

            else:
                in1 = self.add_input_node(pos + '-top')
                in2 = self.add_input_node(pos + '-bottom',
                                          name='Input 1')
                self.inputs.append(in1)
                self.inputs.append(in2)

        elif n_links == 3:
            if 'output' in key:
                out1 = self.add_output_node(pos + '-top')
                out2 = self.add_output_node(pos + '-middle',
                                            name='Output 1')
                out3 = self.add_output_node(pos + '-bottom',
                                            name='Output 2')
                self.outputs.append(out1)
                self.outputs.append(out2)
                self.outputs.append(out3)
            else:
                in1 = self.add_input_node(pos + '-top')
                in2 = self.add_input_node(pos + '-middle',
                                          name='Input 1')
                in3 = self.add_input_node(pos + '-bottom',
                                          name='Input 2')
                self.inputs.append(in1)
                self.inputs.append(in2)
                self.inputs.append(in3)

    @staticmethod
    def get_functions(node_name):
        module = __import__('nn_modules.nn_nodes',
                            fromlist=[node_name + 'Node'])
        _class = getattr(module, node_name + 'Node')

        return _class

    # Split `Stacked Node` properties to separate child's properties
    def set_nodes_properties(self, node_obj, properties):
        for widget in node_obj.sub_layout.children:
            if type(widget) == CustomValueInput or type(widget) == CustomSpinnerInput:
                variable = self.properties[node_obj.name]['properties'][widget.label.text]

                node_obj.properties[widget.label.text][1] = str(variable[1])
                node_obj.properties[widget.label.text][0] = variable[0]

    def set_model_properties(self, model):
        for key in model.keys():
            if key != 'rels' and key != 'beziers_coord':
                try:
                    node_type = key.split(' ')[0]
                    node = self.get_functions(node_type)

                    self.interface_template._node = node
                    node = self.interface_template.add_node2interface(node_name=key,
                                                                      node_type=NORM,
                                                                      has_parent=True)

                    for widget in node.sub_layout.children:
                        if type(widget) == Spinner:
                            node.c_type = self.properties[node.name]['properties']['Layer'][1]

                    self.set_nodes_properties(node_obj=node,
                                              properties=self.properties[key]['properties'])

                except AttributeError as e:
                    raise e

    def load_nodes(self):
        if not self.is_loaded:
            # print(f'Load Nodes: {self.interface_template.nodes()}')
            model = None
            datas = None

            try:
                with open(abspath('models/' + self.name.split(' ')[0] + '.json'), 'r') as f:
                    datas = json.load(f)
                    model = datas['model']
            except FileNotFoundError:
                pass

            if model and datas:
                self.set_model_properties(model)
                self.binding(datas=datas)
            else:
                # print(self.node_template)
                self.set_model_properties(self.node_template['model'])
                self.binding(datas=self.node_template)

            self.is_loaded = True
            # print(self.interface_template.nodes())

    def binding(self, datas=None):
        rels = formatting_rels(datas['rels'], self.interface_template.node_links())

        for rel in rels:
            rel[1].target = rel[0]

            rel[0].target = rel[1]
            nl_index = rel[0].index()
            node_name = rel[0].node.name

            rel[0].target.node.connected_nodes.append(
                f'{node_name} {nl_index}'
            )

            rel[0].connected = 1
            rel[1].connected = 1

    def add_stacked_nodes(self):
        model = self.node_template['model']

        scroll_view = ScrollView(size_hint=(1, 1))
        tree_view = TreeView(size_hint=(1, None),
                             height=25,
                             hide_root=True)
        tree_view.bind(minimum_height=tree_view.setter('height'))
        scroll_view.add_widget(tree_view)

        for node_name in model.keys():
            try:
                tree_node = tree_view.add_node(TreeViewLabel(text=node_name))
                self.properties.update({node_name: {'properties': {},
                                                    'node_class': model[node_name]['node_class'],
                                                    'pos': model[node_name]['pos']}})

                for property_key in model[node_name]['properties'].keys():
                    if property_key != 'Layer':
                        value = str(model[node_name]['properties'][property_key][1])
                        variable_type = model[node_name]['properties'][property_key][0]

                        self.properties[node_name]['properties'].update({property_key: [variable_type, value]})

                        _layout = TreeViewLayout(height=25,
                                                 spacing=20)

                        if variable_type == BOOL_CODE:
                            spinner_form = CustomSpinnerInput(property_name=property_key,
                                                              c_height=self.c_height)
                            spinner_form.input.text = value
                            spinner_form.input.bind(text=partial(self.set_stacked_val,
                                                                 name=property_key,
                                                                 node=node_name))
                            _layout.add_widget(spinner_form)
                        else:
                            input_form = CustomValueInput(name=property_key)
                            input_form.input.text = value
                            input_form.input.bind(text=partial(self.set_stacked_val,
                                                               name=property_key,
                                                               node=node_name))
                            _layout.add_widget(input_form)

                        tree_view.add_node(_layout, tree_node)
                    else:
                        self.properties[node_name]['properties'].update({property_key: [
                            LAYER_CODE,
                            model[node_name]['properties'][property_key][1]]
                        })
            except TypeError:
                pass

        self.sub_layout.rows = 10
        self.add_component(scroll_view)

    def add_kernel_input(self, name=None, default_size=None, _type=MATRIX_CODE):
        if not default_size:
            default_size = (2, 2)

        _layout = BoxLayout(size_hint=(1, None),
                            height=self.c_height,
                            spacing=20)
        self.properties.update({name: [_type, default_size]})

        kernel_input = KernelInput(default_size=default_size)

        _layout.add_widget(Label(text=name,
                                 size_hint=(0.4, 1),
                                 halign='right',
                                 valign='middle',
                                 shorten=True,
                                 max_lines=1))

        _layout.add_widget(kernel_input)
        self.add_component(_layout)

    # CAN BE OPTIMIZED
    def add_list_data(self, name=None, datas=None, _type=BOOL_CODE):
        if not datas:
            datas = [True, False]

        _layout = BoxLayout(size_hint=(1, None),
                            height=self.c_height,
                            spacing=20)
        self.properties.update({name: [_type, datas[0]]})
        _datas = ()

        for i in range(len(datas)):
            _datas += (str(datas[i]),)

        drop_butt = Spinner(text=str(datas[0]),
                            values=_datas,
                            size_hint=(0.6, 1),
                            sync_height=True)
        drop_butt.bind(text=partial(self.set_val, name=name))
        drop_butt.text = str(self.node_template[name][1])

        _layout.add_widget(Label(text=name,
                                 size_hint=(0.4, 1),
                                 halign='right',
                                 valign='middle',
                                 shorten=True,
                                 max_lines=1))

        _layout.add_widget(drop_butt)
        self.add_component(_layout)

    def add_drop_down_list(self):
        self.drop_butt = Spinner(text=self.c_type,
                                 values=self.types,
                                 size_hint=(1, None),
                                 height=self.c_height,
                                 sync_height=True)
        self.drop_butt.bind(text=self.set_type)

        self.add_component(self.drop_butt)

    def set_type(self, obj, text):
        template = self.interface.template['model'][self.name]
        template['properties']['Layer'] = [LAYER_CODE, text]
        self.c_type = text

    def add_component(self, obj):
        self.sub_layout.rows += 1
        self.objs.append(obj)

    def add_id(self):
        self.label = NodeName(size_hint=(1, None),
                              height=self.c_height)
        self.add_component(self.label)

    def add_ib(self):
        self.add_component(Label(height=1,
                                 size_hint=(1, None)))

    def add_val_input(self, name=None, _type=None, default_val=None):
        input_form = CustomValueInput(name=name)
        input_form.input.text = str(self.node_template[name][1])
        input_form.input.bind(text=partial(self.set_val, name=name))

        self.properties.update({name: [_type, str(default_val)]})
        self.add_component(input_form)

    def combine(self):
        self.sub_layout.padding = (20, self.c_padding, 20, self.c_padding)
        self.sub_layout.spacing = self.c_spacing

        for obj in self.objs:
            self.sub_layout.add_widget(obj)

        self.widget_height = self.c_height * self.sub_layout.rows + self.c_padding * 2
        self.widget_height += (self.sub_layout.rows - 1) * self.c_spacing

        self.height = self.widget_height
        self.layout.size = self.size

        # top/bottom of left & right offset
        tblr_offset = (self.height / 3 - 12)

        self.string_pos = {
            'left-top': (-6, (self.height - self.c_height) / 2 + tblr_offset),
            'left-middle': (-6, (self.height - self.c_height) / 2),
            'left-bottom': (-6, (self.height - self.c_height) / 2 - tblr_offset),
            'right-top': (self.width - 6, (self.height - self.c_height) / 2 + tblr_offset),
            'right-middle': (self.width - 6, (self.height - self.c_height) / 2),
            'right-bottom': (self.width - 6, (self.height - self.c_height) / 2 - tblr_offset),
            'top-left': (self.width / 2 - (self.width / 3 - 12), self.height - 6),
            'top-middle': (self.width / 2, self.height - 6),
            'top-right': (self.width / 2 + (self.width / 3 - 12), self.height - 6),
            'bottom-left': (self.width / 2 - (self.width / 3 - 12), -6),
            'bottom-middle': (self.width / 2, -6),
            'bottom-right': (self.width / 2 + (self.width / 3 - 12), -6),
        }

        self.layout.add_widget(self.sub_layout)
        self.add_widget(self.layout)
        self.draw_border()

        self.add_node_links()

    def add_input_node(self, pos: str = 'left-middle', name: str = 'Input 0'):
        input_node = NodeLink(spawn_position=self.string_pos[pos],
                              _type=1,
                              node=self,
                              name=name)
        self.add_widget(input_node)
        return input_node

    def add_output_node(self, pos: str = 'right-middle', name: str = 'Output 0'):
        output_node = NodeLink(spawn_position=self.string_pos[pos],
                               _type=0,
                               node=self,
                               name=name)
        self.add_widget(output_node)
        return output_node

    def draw_border(self):
        with self.canvas:
            # Color(*self.rgba)
            Line(rounded_rectangle=(self.layout.x, self.layout.y,
                                    self.layout.width, self.layout.height,
                                    6))

    def set_stacked_val(self, obj, val, name, node):
        try:
            if val:
                self.interface.template['model'][self.name]['properties'][node]['properties'][name][1] = val
        except Exception as e:
            obj.text = ''

    def set_val(self, obj, val, name):
        try:
            if val:
                self.properties[name][1] = val
        except Exception as e:
            obj.text = ''
