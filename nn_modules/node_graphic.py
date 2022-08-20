from functools import partial

from kivy.graphics import Line
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.scatterlayout import ScatterLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.spinner import Spinner
from kivy.uix.treeview import TreeViewLabel, TreeView, TreeViewNode

from nn_modules.code_names import *
from nn_modules.node_link import NodeLink
from schematics.node_schematic import NodeSchematic
from nn_modules.node_utils import CustomSpinnerInput, KernelInput, CustomValueInput
from utility.rightclick_toolbar.rightclick_toolbar import RightClickMenu
from utility.utils import get_obj


class TreeViewLayout(BoxLayout, TreeViewNode):
    pass


class NodeName(Label):
    def __init__(self, **kwargs):
        super(NodeName, self).__init__(**kwargs)


class NodeGraphic(ScatterLayout):
    c_height = 25
    c_padding = 5
    c_spacing = 5

    n_layer = 0
    b_node = None

    in_list = {}

    def __init__(self, **kwargs):
        super(NodeGraphic, self).__init__()
        self.pos = kwargs.get('spawn_position')
        self.layout = AnchorLayout(anchor_x='center',
                                   anchor_y='center')
        self.layout.padding = (4, 4, 4, 4)
        self.name = kwargs.get('node_name')

        self.sub_layout = GridLayout()
        self.sub_layout.cols = 1
        self.sub_layout.rows = 1

        self.do_scale = False
        self.do_rotation = False
        self.width = 240
        self.widgetHeight = 0

        self.str2pos = {
            LEFT_CODE: 'left',
            RIGHT_CODE: 'right',
            TOP_CODE: 'top',
            BOTTOM_CODE: 'bottom'
        }

        self.layerTypes = ('Input Layer',
                           'Hidden Layer',
                           'Output Layer')
        self.currentLayerType = self.layerTypes[1]

        self.dropDownList = None
        self.label = None

    def open_rightclick_menu(self, obj, touch):
        overlay = get_obj(self.interface, 'Overlay')
        funcs = None

        if touch.button == 'right' and self.collide_point(*touch.pos):
            if self.attributes_get('node_type') == NORM:
                funcs = self.norm_funcs

            elif self.attributes_get('node_type') == STACKED:
                funcs = self.stacked_funcs.copy()
                funcs.update(self.norm_funcs)

            overlay.clear_menu()
            overlay.open_menu(menu_obj=RightClickMenu(funcs=funcs,
                                                      button_width=140,
                                                      pos=overlay.to_overlay_coord(touch, self)))

    def set_val(self, obj, val, _type, name):
        try:
            if val:
                self.properties_set(name, _type, val)
        except Exception as e:
            obj.text = ''

    def set_stacked_val(self, obj, val, key, _type, node_name):
        try:
            if val:
                sub_node = NodeSchematic()
                sub_node.apply_schematic(self.schema['sub_nodes'][node_name])

                sub_node.properties_set(key, _type, val)
        except Exception as e:
            obj.text = ''

    def set_type(self, obj, text):
        # template = self.interface.template['model'][self.name]
        # template['properties']['Layer'] = [LAYER_CODE, text]
        self.layer_set(text)
        setattr(self, 'currentLayerType', text)

    def add_components(self):
        setattr(self, 'label', self.add_id())
        setattr(self, 'dropDownList', self.add_drop_down_list())

        if self.attributes_get('node_type') == STACKED:
            self.add_stacked_nodes()
            # setattr(self, 'type', STACKED)
        else:
            self.sub_layout.row_force_default = True
            self.sub_layout.row_default_height = 25

            for key in self.schema['properties'].keys():
                node_property = self.properties_get(key)

                if node_property[0] in self.code_names:
                    self.add_val_input(name=key,
                                       _type=node_property[0],
                                       default_val=node_property[1])

                elif node_property[0] == BOOL_CODE:
                    self.add_list_data(name=key,
                                       datas=[True, False],
                                       _type=BOOL_CODE)

            # for key in self.node_template.keys():
            #     if key != 'node_type' and 'nl' not in key:
            #         if self.node_template[key][0] in self.code_names:
            #             self.add_val_input(name=key,
            #                                _type=self.node_template[key][0],
            #                                default_val=self.node_template[key][1])
            #
            #         elif self.node_template[key][0] == BOOL_CODE:
            #             self.add_list_data(name=key,
            #                                datas=[True, False],
            #                                _type=BOOL_CODE)
            #
            #         elif self.node_template[key][0] == MATRIX_CODE:
            #             self.add_kernel_input(name=key,
            #                                   default_size=(2, 2),
            #                                   _type=MATRIX_CODE)

    # CAN BE OPTIMIZED
    def add_list_data(self, name=None, datas=None, _type=BOOL_CODE):
        if not datas:
            datas = [True, False]

        _layout = BoxLayout(size_hint=(1, None),
                            height=self.c_height,
                            spacing=20)
        # self.properties.update({name: [_type, datas[0]]})
        self.properties_set(name, _type, datas[0])
        _datas = ()

        for i in range(len(datas)):
            _datas += (str(datas[i]),)

        drop_butt = Spinner(text=str(datas[0]),
                            values=_datas,
                            size_hint=(0.6, 1),
                            sync_height=True)
        drop_butt.bind(text=partial(self.set_val, _type=_type, name=name))
        # drop_butt.text = str(self.node_template[name][1])
        drop_butt.text = str(self.properties_get(name)[1])

        _layout.add_widget(Label(text=name,
                                 size_hint=(0.4, 1),
                                 halign='right',
                                 valign='middle',
                                 shorten=True,
                                 max_lines=1))

        _layout.add_widget(drop_butt)
        self.add_component(_layout)

    def add_drop_down_list(self):
        spinner = Spinner(text=self.currentLayerType,
                          values=self.layerTypes,
                          size_hint=(1, None),
                          height=self.c_height,
                          sync_height=True)
        spinner.bind(text=self.set_type)

        self.add_component(spinner)
        return spinner

    # FIX
    def add_stacked_nodes(self):
        # model = self.node_template['model']
        sub_nodes = self.schema['sub_nodes']

        scroll_view = ScrollView(size_hint=(1, 1))
        tree_view = TreeView(size_hint=(1, None),
                             height=25,
                             hide_root=True)
        tree_view.bind(minimum_height=tree_view.setter('height'))
        scroll_view.add_widget(tree_view)

        for sub_node_name in sub_nodes.keys():
            try:
                sub_node = NodeSchematic()
                sub_node.apply_schematic(sub_nodes[sub_node_name])

                tree_node = tree_view.add_node(TreeViewLabel(text=sub_node_name))

                for key in sub_node.schema['properties'].keys():
                    sub_node_property = sub_node.properties_get(key)
                    variable_type = sub_node_property[0]
                    value = str(sub_node_property[1])

                    _layout = TreeViewLayout(height=25,
                                             spacing=20)

                    if variable_type == BOOL_CODE:
                        widget = CustomSpinnerInput(property_name=key,
                                                    c_height=self.c_height)
                    else:
                        widget = CustomValueInput(name=key)

                    widget.input.text = value
                    widget.input.bind(text=partial(self.set_stacked_val,
                                                   key=key,
                                                   _type=variable_type,
                                                   node_name=sub_node_name))
                    _layout.add_widget(widget)
                    tree_view.add_node(_layout, tree_node)

            except Exception as e:
                raise e

        self.sub_layout.rows = 10
        self.add_component(scroll_view)

    def add_kernel_input(self, name=None, default_size=None, _type=MATRIX_CODE):
        if not default_size:
            default_size = (2, 2)

        _layout = BoxLayout(size_hint=(1, None),
                            height=self.c_height,
                            spacing=20)
        self.properties_set(name, _type, default_size)

        kernel_input = KernelInput(default_size=default_size)

        _layout.add_widget(Label(text=name,
                                 size_hint=(0.4, 1),
                                 halign='right',
                                 valign='middle',
                                 shorten=True,
                                 max_lines=1))

        _layout.add_widget(kernel_input)
        self.add_component(_layout)

    def add_val_input(self, name=None, _type=None, default_val=None):
        input_form = CustomValueInput(name=name)
        input_form.input.text = str(default_val)
        input_form.input.bind(text=partial(self.set_val, _type=_type, name=name))

        self.properties_set(name, _type, default_val)
        self.add_component(input_form)

    def add_input_node(self, pos: (float, float), name: str = 'Input 0'):
        input_node = NodeLink(pos=pos,
                              _type=1,
                              node=self,
                              name=name)

        self.interface.node_links.update({f'{self.name} {name}': input_node})
        self.add_widget(input_node)

        if not self.node_links_get('input'):
            self.node_links_set('input', input_node)

        input_node.schema_set('name', name)
        self.interface.node_links.update({f'{self.name} {input_node.name}': input_node})
        return input_node

    def add_output_node(self, pos: (float, float), name: str = 'Output 0'):
        output_node = NodeLink(pos=pos,
                               _type=0,
                               node=self,
                               name=name)
        self.interface.node_links.update({f'{self.name} {name}': output_node})
        self.add_widget(output_node)

        if not self.node_links_get('output'):
            self.node_links_set('output', output_node)

        output_node.schema_set('name', name)
        self.interface.node_links.update({f'{self.name} {output_node.name}': output_node})
        return output_node

    def add_node_links(self):
        self._add_node_links(self.nl_input_get('n_links'),
                             self.nl_input_get('position'),
                             'nl_input')

        self._add_node_links(self.nl_output_get('n_links'),
                             self.nl_output_get('position'),
                             'nl_output')

    def _add_node_links(self, n_links, position, key):
        pos = self.str2pos[position]

        # top/bottom of left & right offset
        tblr_offset = (self.height / 3 - 12)

        stringPos = {
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

        configurations = [
            ['middle'],
            ['top', 'bottom'],
            ['top', 'middle', 'bottom'],
        ]

        configuration = configurations[n_links - 1]

        for nl_index in range(n_links):
            for config_pos in configuration:
                if 'output' in key:
                    out = self.add_output_node(pos=stringPos[f'{pos}-{config_pos}'])
                    out_schema = self.schema['node_links']['output'][nl_index]

                    if type(out_schema) != dict:
                        out.schema = out_schema.schema
                    else:
                        out.schema = out_schema

                    self.schema['node_links']['output'][nl_index] = out.schema
                    self.outputs.append(out)
                else:
                    _in = self.add_input_node(pos=stringPos[f'{pos}-{config_pos}'])
                    in_schema = self.schema['node_links']['input'][nl_index]

                    if type(in_schema) != dict:
                        _in.schema = in_schema.schema
                    else:
                        _in.schema = in_schema

                    self.schema['node_links']['input'][nl_index] = _in.schema
                    self.inputs.append(_in)

        # print(self.schema)

        # if n_links == 1:
        #     if 'output' in key:
        #         out1 = self.add_output_node(pos=stringPos[f'{pos}-middle'])
        #         out1_schema = self.schema['node_links']['output'][0]
        #         out1_schema.schema_set('node', self)
        #         out1.schema = out1_schema.schema
        #
        #         self.outputs.append(out1)
        #     else:
        #         in1 = self.add_input_node(pos=stringPos[f'{pos}-middle'])
        #         in1_schema = self.schema['node_links']['input'][0]
        #         in1_schema.schema_set('node', self)
        #         in1.schema = in1_schema.schema
        #
        #         self.inputs.append(in1)
        #
        # elif n_links == 2:
        #     if 'output' in key:
        #         out1 = self.add_output_node(pos=stringPos[f'{pos}-top'])
        #         out1_schema = self.schema['node_links']['output'][0]
        #         out1_schema.schema_set('node', self)
        #         out1.schema = out1_schema.schema
        #
        #         out2 = self.add_output_node(pos=stringPos[f'{pos}-bottom'],
        #                                     name='Output 1')
        #         out2_schema = self.schema['node_links']['output'][1]
        #         out2_schema.schema_set('node', self)
        #         out2.schema = out2_schema.schema
        #
        #         self.outputs.append(out1)
        #         self.outputs.append(out2)
        #
        #     else:
        #         in1 = self.add_input_node(pos=stringPos[f'{pos}-top'])
        #         in1_schema = self.schema['node_links']['input'][0]
        #         in1_schema.schema_set('node', self)
        #         in1.schema = in1_schema.schema
        #
        #         in2 = self.add_input_node(pos=stringPos[f'{pos}-bottom'],
        #                                   name='Input 1')
        #         in2_schema = self.schema['node_links']['input'][1]
        #         in2_schema.schema_set('node', self)
        #         in2.schema = in2_schema.schema
        #
        #         self.inputs.append(in1)
        #         self.inputs.append(in2)
        #
        # elif n_links == 3:
        #     if 'output' in key:
        #         out1 = self.add_output_node(pos=stringPos[f'{pos}-top'])
        #         out1_schema = self.schema['node_links']['output'][0]
        #         out1_schema.schema_set('node', self)
        #         out1.schema = out1_schema.schema
        #
        #         out2 = self.add_output_node(pos=stringPos[f'{pos}-middle'],
        #                                     name='Output 1')
        #         out2_schema = self.schema['node_links']['output'][1]
        #         out2_schema.schema_set('node', self)
        #         out2.schema = out2_schema.schema
        #
        #         out3 = self.add_output_node(pos + '-bottom',
        #                                     name='Output 2')
        #         out3_schema = self.schema['node_links']['output'][2]
        #         out3_schema.schema_set('node', self)
        #         out3.schema = out3_schema.schema
        #
        #         self.outputs.append(out1)
        #         self.outputs.append(out2)
        #         self.outputs.append(out3)
        #     else:
        #         in1 = self.add_input_node(pos=stringPos[f'{pos}-top'])
        #         in1_schema = self.schema['node_links']['input'][0]
        #         in1_schema.schema_set('node', self)
        #         in1.schema = in1_schema.schema
        #
        #         in2 = self.add_input_node(pos=stringPos[f'{pos}-middle'],
        #                                   name='Input 1')
        #         in2_schema = self.schema['node_links']['input'][1]
        #         in2_schema.schema_set('node', self)
        #         in2.schema = in2_schema.schema
        #
        #         in3 = self.add_input_node(pos=stringPos[f'{pos}-bottom'],
        #                                   name='Input 2')
        #         in3_schema = self.schema['node_links']['input'][2]
        #         in3_schema.schema_set('node', self)
        #         in3.schema = in3_schema.schema
        #
        #         self.inputs.append(in1)
        #         self.inputs.append(in2)
        #         self.inputs.append(in3)

    def add_component(self, obj):
        self.sub_layout.rows += 1
        self.graphicObjs.append(obj)

    def add_id(self):
        label = NodeName(size_hint=(1, None),
                         height=self.c_height,
                         text=self.name)
        self.add_component(label)
        return label

    def add_ib(self):
        self.add_component(Label(height=1,
                                 size_hint=(1, None)))

    def combine(self):
        self.sub_layout.padding = (20, self.c_padding, 20, self.c_padding)
        self.sub_layout.spacing = self.c_spacing

        for obj in self.graphicObjs:
            self.sub_layout.add_widget(obj)

        self.widgetHeight = self.c_height * self.sub_layout.rows + self.c_padding * 2
        self.widgetHeight += (self.sub_layout.rows - 1) * self.c_spacing

        self.height = self.widgetHeight
        self.layout.size = self.size

        self.layout.add_widget(self.sub_layout)
        self.add_widget(self.layout)
        self.draw_border()
        self.add_node_links()

    # Draw border of the node
    def draw_border(self):
        with self.canvas:
            # Color(*self.rgba)
            Line(rounded_rectangle=(self.layout.x, self.layout.y,
                                    self.layout.width, self.layout.height,
                                    6))
