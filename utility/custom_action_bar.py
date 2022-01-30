import json
from functools import partial

from kivy.clock import Clock
from kivy.graphics import Bezier
from kivy.uix.actionbar import ActionBar, ActionButton, ActionPrevious, ActionView, ActionDropDown, ActionGroup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.checkbox import CheckBox
from kivy.uix.popup import Popup
from kivy.uix.spinner import Spinner

from custom_filechooser.custom_filechooser import FileChooser
from nn_modules.code_names import NORM, STACKED
from nn_modules.node import CustomValueInput, NodeLink
from node_editor.node_editor import NodeEditor
from utility.utils import get_obj
from settings.config import configs


class CustomSpinnerInput(BoxLayout):
    def __init__(self, c_height=None, default_halign='center', **kwargs):
        super(CustomSpinnerInput, self).__init__()
        self.size_hint = (1, None)
        self.height = c_height
        self.spacing = 20

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


class CustomActionBar(ActionBar):
    def __init__(self, **kwargs):
        super(CustomActionBar, self).__init__()
        self.size_hint_y = 0.032
        self.spacing = 3

        self.action_view = ActionView()

        self.new_button_options = {'Training Algorithm': (self.create_algorithms, 0),
                                   'Evaluating Algorithm': (self.create_algorithms, 1),
                                   'Node': self.create_node,
                                   'Processor': (self.create_algorithms, -1)}

        # New Button
        self.new_button_dropdown = ActionDropDown()
        self.new_button_dropdown.size_hint_x = None
        self.new_button_dropdown.width = 200
        self.new_button_dropdown.auto_width = False

        self.new_button = ActionButton(text='New...')
        self.new_button.bind(on_release=self.new_button_dropdown.open)

        for key in self.new_button_options.keys():
            button = Button(text=key,
                            size_hint_y=None,
                            height=44,
                            width=200)

            ftype = type(self.new_button_options[key])
            if ftype == tuple:
                button.bind(on_release=partial(self.new_button_options[key][0],
                                               _type=self.new_button_options[key][1]))
            else:
                button.bind(on_release=self.new_button_options[key])

            self.new_button_dropdown.add_widget(button)

        self.file_chooser_popup = Popup(size_hint=(0.6, 0.6),
                                        title='Models')
        self.file_chooser = FileChooser(component_panel=kwargs.get('component_panel'))
        self.file_chooser.bind(on_submit=self.load_model)
        self.file_chooser_popup.content = self.file_chooser

        self.save_button = ActionButton(text='Save File', size_hint_x=0.05)
        self.save_button.bind(on_release=self.save_model)

        self.load_button = ActionButton(text='Load File', size_hint_x=0.05)
        self.load_button.bind(on_release=lambda obj: self.file_chooser_popup.open())
        self.load_button.bind(on_release=lambda obj: self.file_chooser_popup.open())

        # self.setting_button.add_widget(self.setting_button_view)

        self.action_view.add_widget(self.save_button)
        self.action_view.add_widget(self.load_button)
        self.action_view.add_widget(self.new_button)

        self.action_view.add_widget(ActionPrevious(size_hint_x=None,
                                                   width=0,
                                                   app_icon_width=0.1,
                                                   with_previous=False,
                                                   app_icon=''))
        # self.add_widget(Label(size_hint_x=1))
        self.add_widget(self.action_view)

    def create_node(self, obj):
        screen_manager = get_obj(self, '_Container').request_obj('Manager')
        component_panel = get_obj(self, '_Container').request_obj('ComponentPanel')

        node_editor = NodeEditor(screen_manager=screen_manager,
                                 component_panel=component_panel)
        node_editor.open()

    def create_algorithms(self, obj, _type):
        screen_manager = get_obj(self, '_Container').request_obj('Manager')
        tab_manager = screen_manager.get_screen('scripting').children[-1].children[1]
        # component_panel = get_obj(self, 'ComponentPanel')

        source = 'example_functions'
        fpath = None

        if _type == 0:
            fpath = f'{source}\\training_function_template.txt'

        elif _type == 1:
            fpath = f'{source}\\evaluating_function_template.txt'

        with open(f'hyper_variables_forms\\{fpath}', 'r') as f:
            code_template = f.read()

        screen_manager.current = 'scripting'

        tab_manager.add_tab(func_name=obj.text,
                            _fkwargs={'text': code_template})

        tab = tab_manager.tab_list[-1]
        tab_manager.switch_to(tab)

    # component_panel._update_panel()

    def get_hvfs(self, interface):
        hvfs = get_obj(interface, 'IToolBar')
        hvfs_properties = {}

        for tab in hvfs.tab_list:
            # print(tab.text)
            # print(tab.content)
            current_func = tab.content.children[1].text
            hvfs_properties.update({tab.text: {current_func: {}}})

            for obj in tab.content.children:
                if type(obj) == GridLayout:
                    for children in obj.children:
                        hvfs_properties[tab.text][current_func].update({children.name: str(children.value)})

        return hvfs_properties

    @staticmethod
    def get_beziers_points(interface=None):
        coordinates = []

        for children in interface.scatter_plane.canvas.children:
            if type(children) == Bezier:
                coordinates.append([children.points[0:2], children.points[-2:]])
        return coordinates

    @staticmethod
    def get_nodes(node_name):
        module = __import__('nn_modules.nn_nodes',
                            fromlist=[node_name + 'Node'])
        _class = getattr(module, node_name + 'Node')

        return _class

    def load_hvfs(self, datas, interface):
        itoolbar = get_obj(interface, 'IToolBar')
        hvfs = interface.hvfs = datas['hvfs']

        for tab in itoolbar.tab_list:
            for form_type in hvfs.keys():
                if tab.text == form_type:
                    itoolbar.switch_to(tab, do_scroll=True)
                    current_function = tab.content.children[1].text = [key for key in hvfs[form_type].keys()][0]
                    properties_form = tab.content.children[0]

                    for children in properties_form.children:
                        for _property in hvfs[form_type][current_function].keys():
                            if children.name == _property:
                                children.value = hvfs[form_type][current_function][_property]
                                children.input.text = children.value

    def load_model(self, obj, selection, touch):
        interface_tab_manager = get_obj(self, 'InterfaceTabManager')

        func_name = selection[0].split('\\')[-1].split('.')[0]
        interface_tab_manager.add_tab(func_name=func_name,
                                      _fkwargs={})

        # Add nodes 1 frame after tab_manager.add_tab function is called
        Clock.schedule_once(partial(self.add_nodes,
                                    interface_tab_manager,
                                    func_name,
                                    selection), 0)

    # Clock.schedule_once(partial(self.set_model_name, tab_manager, func_name), 0)

    @staticmethod
    def set_stacked_node_properties(node_obj, properties, *args):
        scroll_view = node_obj.sub_layout.children[1]
        tree_view = scroll_view.children[0]

        for widget in node_obj.sub_layout.children:
            if type(widget) == Spinner:
                node_obj.c_type = widget.text = properties['Layer'][1]

        for parent_node in tree_view.children:
            for leaf in parent_node.nodes:
                for widget in leaf.children:
                    if type(widget) != Spinner:
                        value = str(properties[parent_node.text]['properties'][widget.label.text][1])

                        widget.input.text = value
                        # node_obj.properties[parent_node.text]['properties'][widget.label.text] = value

    @staticmethod
    def set_nodes_properties(node_obj, properties, *args):
        for widget in node_obj.sub_layout.children:
            if type(widget) == CustomValueInput:
                value = str(properties[widget.label.text][1])

                widget.input.text = value
                node_obj.properties[widget.label.text][1] = value

            elif type(widget) == Spinner:
                node_obj.c_type = widget.text = properties['Layer'][1]

            elif type(widget) == CustomSpinnerInput:
                value = str(properties[widget.label.text][1])

                widget.input.text = value
                node_obj.properties[widget.label.text][1] = value

    @staticmethod
    def set_model_name(interface, func_name, *args):
        interface.model_name_input.text = func_name

    def add_nodes(self, tab_manager, func_name, selection, *args):
        interface = tab_manager.current_tab.content.children[-1]
        interface.model_name_input.text = ''

        Clock.schedule_once(partial(self.set_model_name, interface, func_name), 0)

        with open(selection[0], 'r') as f:
            datas = json.load(f)

            for key in datas['model'].keys():
                try:
                    node_type = key.split(' ')[0]
                    node = self.get_nodes(node_type)

                    interface._node = node
                    node = interface.add_node2interface(
                        spawn_position=datas['model'][key]['pos']
                    )

                    interface.create_template(node)

                    if node.type == NORM:
                        Clock.schedule_once(partial(self.set_nodes_properties,
                                                    node,
                                                    datas['model'][key]['properties']), 1)
                    elif node.type == STACKED:
                        node.properties = datas['model'][key]['properties']
                        Clock.schedule_once(partial(self.set_stacked_node_properties,
                                                    node,
                                                    datas['model'][key]['properties']), 1)

                    # self.set_nodes_properties(node_obj=node_obj,
                    #                           properties=datas[key]['properties'],
                    #                           interface=interface)

                except AttributeError as e:
                    pass

            # interface.draw()
            if 'mapped_path' in datas.keys():
                interface.str_mapped_path = datas['mapped_path']
                interface.is_trained = True

            self.draw_beziers(datas=datas,
                              interface=interface)
            self.load_hvfs(datas=datas,
                           interface=interface)

    @staticmethod
    def formatting_rels(rels, node_links):
        formatted_rels = []
        current_rel = []

        for rel in rels:
            for rel_name in rel:
                for node_link in node_links:
                    if f'{node_link.node.name} {node_link.name}' == rel_name:
                        # print(f'{node_link.node.name} {node_link.name}')
                        current_rel.append(node_link)

                    if len(current_rel) == 2:
                        formatted_rels.append(current_rel)
                        current_rel = []

        return formatted_rels

    # TODO: FIX BEZIERS LINE
    def draw_beziers(self, datas, interface):
        rels = self.formatting_rels(datas['rels'], interface.node_links())

        # for coord, rel in zip(datas['beziers_coord'], rels):
        for coord, rel in zip(datas['beziers_coord'], rels):
            # coord = self.get_rels_pos(rel, interface)
            # spl = get_obj(interface, 'ScatterPlaneLayout')

            # Touch Down
            # coord.append(spl.to_parent(*rel[0].pos))
            rel[0].node._bind(nav=rel[0].link_type)
            rel[0].c_pos = coord[0]

            # Touch Up
            # coord.append(spl.to_widget(*rel[1].pos))
            rel[1].node._bind(state=2,
                              nav=rel[1].link_type)
            rel[1].c_pos = coord[1]
            rel[1].target = rel[0]
            rel[1].t_pos = rel[0].c_pos

            rel[0].t_pos = coord[0]
            rel[0].target = rel[1]

            nl_index = rel[0].index()
            node_name = rel[0].node.name

            rel[0].target.node.connected_nodes.append(
                f'{node_name} {nl_index}'
            )

            rel[0].connected = 1
            rel[1].connected = 1

            # Draw Bezier
            # print(coord)
            bezier = interface.draw(*coord)

            # rel[0].node.beziers['output'] = rel[1].node.beziers['input'] = bezier

            interface.links.append([rel[1], rel[0], bezier])
            interface.instructions.append(bezier)
            # interface.bezier_points = datas['beziers_coord']
            interface.rels = datas['rels']

    def save_nodes_pos(self, template, interface):
        for node in get_obj(self, 'Interface').nodes():
            template['model'][node.name].update({'pos': node.pos})

        return template

    def save_model(self, obj):
        model_name = None
        tab_manager = get_obj(self, 'InterfaceTabManager')
        interface = get_obj(self, 'Interface')

        try:
            model_name = interface.model_name
            tab_manager.current_tab.text = model_name

        except AttributeError as e:
            if 'model_name' in str(e):
                model_name = tab_manager.current_tab.text

        tab_manager.tab_name_list.append(model_name)
        # print(interface.template)

        # model = interface.m_list
        # sorter = Sorter()
        # sorted_model = sorter.sort(model)

        # interface.template.update({'relationship': interface.mn_list,
        #                            'links_pos': [bezier.points for bezier in interface.beziers]})
        # interface.template.update({'relationship': interface.mn_list})
        # self.get_nodes_pos()
        interface.template.update({'beziers_coord': self.get_beziers_points(interface=interface),
                                   'rels': interface.rels,
                                   'hvfs': self.get_hvfs(interface)})
        interface.template = self.save_nodes_pos(interface.template,
                                                 interface)

        if interface.is_trained:
            interface.template.update({
                'mapped_path': interface.str_mapped_path
            })

        with open('{0}\\{1}.json'.format(configs['models_path'],
                                         model_name), 'w') as f:
            json.dump(interface.template,
                      f,
                      sort_keys=True,
                      indent=4)

        self.file_chooser._update_files()
