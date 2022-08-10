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
            if self.type == NORM:
                funcs = self.norm_funcs
            elif self.type == STACKED:
                funcs = self.stacked_funcs.copy()
                funcs.update(self.norm_funcs)

            overlay.clear_menu()
            overlay.open_menu(menu_obj=RightClickMenu(funcs=funcs,
                                                      button_width=140,
                                                      pos=overlay.to_overlay_coord(touch, self)))

    def set_val(self, obj, val, name):
        try:
            if val:
                self.properties[name][1] = val
        except Exception as e:
            obj.text = ''

    def set_type(self, obj, text):
        template = self.interface.template['model'][self.name]
        template['properties']['Layer'] = [LAYER_CODE, text]
        setattr(self, 'currentLayerType', text)

    def add_components(self):
        setattr(self, 'label', self.add_id())
        setattr(self, 'dropDownList', self.add_drop_down_list())

        if self.node_template['node_type'] == STACKED:
            self.add_stacked_nodes()
            setattr(self, 'type', STACKED)
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
        spinner = Spinner(text=self.currentLayerType,
                          values=self.layerTypes,
                          size_hint=(1, None),
                          height=self.c_height,
                          sync_height=True)
        spinner.bind(text=self.set_type)

        self.add_component(spinner)
        return spinner

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

                self.properties.update({
                    'rels': self.node_template['rels'],
                    'beziers_coord': self.node_template['beziers_coord'],
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

    def add_val_input(self, name=None, _type=None, default_val=None):
        input_form = CustomValueInput(name=name)
        input_form.input.text = str(self.node_template[name][1])
        input_form.input.bind(text=partial(self.set_val, name=name))

        self.properties.update({name: [_type, str(default_val)]})
        self.add_component(input_form)

    def add_input_node(self, pos: (float, float), name: str = 'Input 0'):
        input_node = NodeLink(pos=pos,
                              _type=1,
                              node=self,
                              name=name)
        self.add_widget(input_node)
        return input_node

    def add_output_node(self, pos: (float, float), name: str = 'Output 0'):
        output_node = NodeLink(pos=pos,
                               _type=0,
                               node=self,
                               name=name)
        self.add_widget(output_node)
        return output_node

    def add_node_links(self):
        self._add_node_links(self.node_template['nl_input']['n_links'],
                             self.node_template['nl_input']['position'],
                             'nl_input')

        self._add_node_links(self.node_template['nl_output']['n_links'],
                             self.node_template['nl_output']['position'],
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

        if n_links == 1:
            if 'output' in key:
                out1 = self.add_output_node(pos=stringPos[f'{pos}-middle'])
                self.outputs.append(out1)
            else:
                in1 = self.add_input_node(pos=stringPos[f'{pos}-middle'])
                self.inputs.append(in1)

        elif n_links == 2:
            if 'output' in key:
                out1 = self.add_output_node(pos=stringPos[f'{pos}-top'])
                out2 = self.add_output_node(pos=stringPos[f'{pos}-bottom'],
                                            name='Output 1')
                self.outputs.append(out1)
                self.outputs.append(out2)

            else:
                in1 = self.add_input_node(pos=stringPos[f'{pos}-top'])
                in2 = self.add_input_node(pos=stringPos[f'{pos}-bottom'],
                                          name='Input 1')
                self.inputs.append(in1)
                self.inputs.append(in2)

        elif n_links == 3:
            if 'output' in key:
                out1 = self.add_output_node(pos=stringPos[f'{pos}-top'])
                out2 = self.add_output_node(pos=stringPos[f'{pos}-middle'],
                                            name='Output 1')
                out3 = self.add_output_node(pos + '-bottom',
                                            name='Output 2')
                self.outputs.append(out1)
                self.outputs.append(out2)
                self.outputs.append(out3)
            else:
                in1 = self.add_input_node(pos=stringPos[f'{pos}-top'])
                in2 = self.add_input_node(pos=stringPos[f'{pos}-middle'],
                                          name='Input 1')
                in3 = self.add_input_node(pos=stringPos[f'{pos}-bottom'],
                                          name='Input 2')
                self.inputs.append(in1)
                self.inputs.append(in2)
                self.inputs.append(in3)

    def add_component(self, obj):
        self.sub_layout.rows += 1
        self.graphicObjs.append(obj)

    def add_id(self):
        label = NodeName(size_hint=(1, None),
                         height=self.c_height)
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
