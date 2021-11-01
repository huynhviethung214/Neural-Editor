import json

from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stencilview import StencilView
from kivy.uix.scatterlayout import ScatterPlaneLayout
from kivy.uix.treeview import TreeViewLabel, TreeView
from kivy.uix.spinner import Spinner
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.graphics import Bezier
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window

from kivy.config import Config

# import datasets_processors.generate_processors

from nn_modules.node import NodeLink, Node
from node_editor.node_editor import NodeEditor
from utility.custom_action_bar import CustomActionBar
from utility.utils import get_obj
from utility.custom_tabbedpanel import TabManager
from utility.custom_input.custom_input import CustomTextInput
from i_modules.interface_actionbar.interface_actionbar import TrainButton, _ProgressBar, \
                                                            IndicatorLabel, CheckpointButton
from nn_modules.code_names import *
from hyper_variables_forms.hvfs import *

Config.set('input', 'mouse', 'mouse,disable_multitouch')


# ADDING FEATURES TO SETTING SCREEN (2)
# GROUP MULTIPLE NODES IN TO A BLOCK (1)
# CREATE A NEW DYNAMIC AND CUSTOMIZABLE TRAINING AND EVALUTING FUNCTIONS (3)


class InvisObj(Widget):
    def __init__(self, **kwargs):
        super(InvisObj, self).__init__()
        self.size_hint = (0.3, 0.05)


class CreateBlock(BoxLayout):
    def create_block(self):
        screen_manager = get_obj(self, '_Container').request_obj('Manager')
        component_panel = get_obj(self, '_Container').request_obj('ComponentPanel')

        node_editor = NodeEditor(screen_manager=screen_manager,
                                 component_panel=component_panel)
        node_editor.open()


class ComponentPanel(ScrollView):
    def __init__(self, **kwargs):
        super(ComponentPanel, self).__init__()
        self.size_hint = (1, 1)
        self.tree_view = TreeView(size_hint=(1, None),
                                  hide_root=True)
        self.tree_view.bind(minimum_height=self.tree_view.setter('height'))
        # self.tree_view.root_options = {'text': 'Component Panel'}

        nodes_file_path = []

        self.norm_nodes_label = TreeViewLabel(text='Normal Nodes')
        self.group_nodes_label = TreeViewLabel(text='Stacked Nodes')
        self.special_nodes_label = TreeViewLabel(text='Functions')

        self.tree_view.add_node(self.norm_nodes_label)
        self.tree_view.add_node(self.group_nodes_label)
        self.tree_view.add_node(self.special_nodes_label)
        self.add_widget(self.tree_view)
        self.update_panel()

    def get_node_names(self):
        node_names = []

        for node in self.tree_view.iterate_all_nodes():
            if type(node) != TreeViewLabel:
                node_names.append(node.text)

        return node_names

    def update_panel(self):
        c_label = None

        with open('nn_modules\\nn_nodes.json', 'r') as f:
            nodes = json.load(f)

            for node_name in nodes.keys():
                if node_name not in self.get_node_names():
                    module = __import__('nn_modules.nn_components',
                                        fromlist=[node_name])
                    _class = getattr(module, node_name)

                    if nodes[node_name]['node_type'] == 8:
                        c_label = self.special_nodes_label

                    elif nodes[node_name]['node_type'] == 9:
                        c_label = self.group_nodes_label

                    elif nodes[node_name]['node_type'] == 10:
                        c_label = self.norm_nodes_label

                    self.tree_view.add_node(_class(interface=Interface),
                                            parent=c_label)


class SIToolBar(BoxLayout):
    pass


class IToolBar(TabbedPanel):
    _children = []


class Interface(StencilView, GridLayout):
    def __init__(self, **kwargs):
        super(Interface, self).__init__()
        self.size_hint = (1, 1)
        self.m_list = []
        self.mn_list = []
        self.node_names = []

        self.current_bezier_pos = []
        self.bezier_points = []
        self.rels = []

        # self.current_bz_point = []

        self.current_node_down = None
        self._node = None
        self._state = 0
        # self._spos = (0, 0)

        self.rows = 2
        self.cols = 3

        self.ori = (0, 0)
        self.end = (0, 0)

        self.connected_node_link = None
        self.is_drawing = 0
        self.current_bezier = None

        self.links = []
        self.instructions = []
        self.template = {}

        self.output_node = None

        self.action_bar = SIToolBar()

        self.model_name_input = CustomTextInput(size_hint_x=0.3,
                                                max_length=50)
        self.model_name_input.bind(text=lambda obj, text: setattr(Interface,
                                                                  'model_name',
                                                                  text))

        self.add_widget(Widget(size_hint=(0.3, 0.05)))
        self.add_widget(Widget(size_hint=(0.3, 0.05)))
        self.add_action_bar()

        self.add_widget(Widget())
        self.add_scatter_plane()

        # self.add_progress_bar()
        # self.add_widget(_ProgressBar(size_hint_x=0.6))
        # self.add_widget(Widget())

        # self.add_widget(Widget(size_hint=(0.3, 0.05)))
        # self.add_widget(Widget(size_hint=(0.3, 0.05)))
        # self.add_widget(_ProgressBar(size_hint=(0.3, 0.05)))

        self.bind(on_touch_up=self.add_node)
        self.bind(on_touch_move=self.unbind)

        # self.bind(on_touch_move=self._is_move_validate)
        Window.bind(mouse_pos=self._is_in_bbox)
        # self.bind(on_touch_up=self._is_up_validate)
        # self.bind(on_touch_down=self._is_down_validate)

        self.bind(on_touch_move=self._draw_link)
        self.bind(on_touch_move=self._update_canvas)

        self.bind(on_touch_down=self.node_link_down)
        self.bind(on_touch_up=self.node_link_up)

    def add_progress_bar(self):
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(Label(size_hint_y=0.95))
        layout.add_widget(_ProgressBar(size_hint_y=0.05))
        self.add_widget(layout)

    def add_action_bar(self):
        self.action_bar.add_widget(self.model_name_input)
        self.action_bar.add_widget(CheckpointButton(interface=self))
        self.action_bar.add_widget(TrainButton())
        # self.action_bar.add_widget(Terminate())
        # self.action_bar.add_widget(_ProgressBar(size_hint_x=0.1))
        # self.action_bar.add_widget(IndicatorLabel())

        self.add_widget(self.action_bar)

    def add_scatter_plane(self):
        self.scatter_plane = ScatterPlaneLayout()

        self.scatter_plane.do_rotation = False
        self.scatter_plane.do_scale = False
        self.scatter_plane.do_scroll = False
        self.scatter_plane.do_translation = False

        self.add_widget(self.scatter_plane)

    def check_nl_collision(self, touch):
        try:
            for node in self.scatter_plane.children:
                for node_link in node.children[0].children:
                    if type(node_link) == NodeLink:
                        pos = node_link.to_widget(*touch.pos)

                        if node_link.collide_point(*pos):
                            return True, node, node_link

            return False, None, None

        except IndexError:
            pass

    def unbind(self, obj, touch):
        if touch.button == 'left':
            try:
                _, node, node_link = self.check_nl_collision(touch=touch)

                if node_link is not None:
                    if self.is_drawing and node_link.target is not None:
                        for info in self.links:
                            if node_link in info and node_link.target in info:
                                try:
                                    self.instructions.remove(info[-1])
                                    # self.clear_canvas()

                                    # Custom Event
                                    node_link.connected = 0

                                    node.unbind(node_link, node_link.link_type)
                                    self.links.remove(info)

                                except ValueError:
                                    pass
                    return True

            except TypeError:
                pass

    def node_link_up(self, obj, touch):
        if touch.button == 'left':
            try:
                valid, node, node_link = self.check_nl_collision(touch=touch)

                if valid:
                    if node_link.link_type == 1 and not node_link.connected:
                        node._bind(state=2,
                                   nav=node_link.link_type)
                        # pos = self.get_pos(node_link, node_link.pos)
                        pos = self.scatter_plane.to_local(*touch.pos)

                        node_link.c_pos = pos
                        node_link.target = self.connected_node_link
                        node_link.t_pos = self.connected_node_link.c_pos  # WILL BE DEPRECATED IN FUTURE VERSION
                        node_link.connected = 1

                        # TODO: IMPORTANT!!!!!!!!!!
                        self.connected_node_link.t_pos = pos
                        self.connected_node_link.target = node_link

                        nl_index = self.connected_node_link.index()
                        node_name = self.connected_node_link.node.name

                        # # TODO: ADDED FEATURE (26/9/2021)
                        # self.connected_node_link.connecting_nodes.insert(node, nl_index)

                        self.connected_node_link.target.node.connected_nodes.append(
                            f'{node_name} {nl_index}'
                        )

                        # _pos = (pos[0] + 5, pos[1] + 5)
                        _pos = pos
                        bezier = self.draw(self.ori, _pos)

                        # NEW FEATURES
                        self.rels.append([self.current_node_down,
                                          f'{node.name} {node_link.name}'])
                        self.current_bezier_pos.append(pos)
                        # self.bezier_points.append([[self.ori[0] - 5, self.ori[1] - 5], pos])
                        # print(self.current_bezier_pos)
                        self.bezier_points.append(self.current_bezier_pos)
                        self.current_bezier_pos = []
                        # print(self.rels)

                        node.beziers['input'] = self.output_node.beziers['output'] = bezier

                        node_link.connected = 1
                        node_link.target.connected = 1

                        self.links.append([node_link, self.connected_node_link, bezier])
                        self.instructions.append(bezier)

                        self.is_drawing = 0

                        # print(node.connected_nodes)
                        # print(node.name)

                    return True

                elif not valid and self.is_drawing:
                    self.clear_canvas()
                    self.is_drawing = 0

                return False

            except TypeError:
                pass

    def node_link_down(self, obj, touch):
        # print(self.collide_point(*touch.pos) and not self.action_bar.collide_point(*self.to_widget(*touch.pos)))
        if touch.button == 'left':
            try:
                valid, node, node_link = self.check_nl_collision(touch=touch)

                if valid:
                    if node_link.link_type == 0 and not node_link.connected:
                        node._bind(nav=node_link.link_type)

                        # pos = self.get_pos(node_link, node_link.pos)
                        pos = self.scatter_plane.to_local(*touch.pos)
                        node_link.c_pos = pos

                        self.connected_node_link = node_link
                        self.output_node = node

                        # self.ori = (pos[0] + 5, pos[1] + 5)
                        self.ori = pos
                        self.current_bezier_pos.append(pos)
                        self.current_node_down = f'{node.name} {node_link.name}'

                        self.is_drawing = 1

                    elif node_link.link_type == 1 and node_link.connected:
                        bezier = node.beziers['input']
                        self.instructions.remove(bezier)
                        self.ori = node_link.target.c_pos

                        self.connected_node_link = node_link.target
                        self.output_node = node_link.target.node

                        node_link.target.connected = 0
                        node_link.connected = 0

                        node.unbind(node_link, node_link.link_type)
                        self.is_drawing = 1

                    return True

                return False

            except TypeError:
                pass

    def draw(self, ori=None, end=None):
        self.clear_canvas()
        self.scatter_plane.canvas.ask_update()

        with self.scatter_plane.canvas:
            bezier = Bezier(points=(ori[0], ori[1],
                                    (end[0] + ori[0]) / 2 + 20, ori[1],
                                    (end[0] + ori[0]) / 2 - 20, end[1],
                                    end[0], end[1]),
                            segments=800)
            return bezier

    def _draw_link(self, obj, touch):
        if self.is_drawing:
            self.draw(self.ori, self.scatter_plane.to_local(*touch.pos))

    def clear_canvas(self):
        if len(self.scatter_plane.canvas.children) > 1:
            for ins in self.scatter_plane.canvas.children:
                if type(ins) == Bezier and ins not in self.instructions:
                    self.scatter_plane.canvas.remove(ins)

    def get_pos(self, obj, pos):
        pos = self.scatter_plane.to_local(*obj.to_window(*pos))
        return pos

    def _is_in_bbox(self, obj, pos):
        _pos = self.to_widget(*pos)

        if self.collide_point(*_pos) and not self.action_bar.collide_point(*_pos):
            self.scatter_plane.do_translation = True
        else:
            self.scatter_plane.do_translation = False

        return True

    def remove_node(self, node):
        self.children[0].remove_widget(node)
        self.template.pop(node.name)

        remove_list = []

        for pair in self.m_list:
            if node in pair:
                remove_list.append(pair)

        for pair in remove_list:
            self.m_list.remove(pair)

    def add_node_names(self, node=None):
        node_name = str(node)
        node_name = node_name.split(' ')[0]
        node_name = node_name.split('.')[-1]
        node_name = node_name[0:-4]
        self.node_names.append(node_name)
        # print(self.node_names)

    def node_links(self):
        _node_links = []

        for node in self.nodes():
            for widget in node.children[0].children:
                if type(widget) == NodeLink:
                    _node_links.append(widget)

        return _node_links

    def nodes(self):
        _nodes = []

        for widget in self.children[0].children:
            if 'Node' in str(widget):
                _nodes.append(widget)

        return _nodes

    def add_node2interface(self, spawn_position):
        spl = get_obj(self, 'ScatterPlaneLayout')
        node_obj = self._node(spawn_position=spawn_position,
                              interface=self)
        self.add_node_names(node=node_obj)
        spl.add_widget(node_obj)
        self._state = 0
        self._node = None

        return node_obj

    def add_node(self, obj, touch):
        # print(_self.collide_point(*touch.pos) and not _self.action_bar.collide_point(*_self.to_widget(*touch.pos)))
        if self.collide_point(*touch.pos):
            if self._state == 1:
                spl = get_obj(self, 'ScatterPlaneLayout')
                pos = spl.to_local(*touch.pos)

                node_obj = self.add_node2interface(spawn_position=pos)

                # Interface.model = Node.m_list
                self.create_template(node_obj)
            # print(self.template)

        return True

    def _update_canvas(self, obj, touch):
        try:
            if self.collide_point(*self.to_widget(*obj.pos)) and len(
                    self.scatter_plane.children) >= 2 and not self.is_drawing and touch.button == 'left':
                for node in self.scatter_plane.children:
                    for node_link in node.children[0].children:
                        if type(node_link) == NodeLink:
                            for info in self.links:
                                if node_link in info and node_link.target in info:
                                    for bezier in self.scatter_plane.canvas.children:
                                        if bezier in info:
                                            _pos = self.get_pos(node_link, node_link.pos)

                                            if _pos != node_link.c_pos and node_link.t_pos is not None:
                                                ori = (node_link.t_pos[0] + 5, node_link.t_pos[1] + 5)
                                                end = (_pos[0] + 5, _pos[1] + 5)

                                                bezier.points = (ori[0], ori[1],
                                                                 (end[0] + ori[0]) / 2 + 20, ori[1],
                                                                 (end[0] + ori[0]) / 2 - 20, end[1],
                                                                 end[0], end[1])

                                                node_link.c_pos = _pos
                                                node_link.target.t_pos = _pos

        except IndexError:
            pass

    def create_template(self, node=None):
        node_properties = {}
        obj_name = None
        node_properties.update(node.properties)

        for obj in node.sub_layout.children:
            if type(obj) == Spinner:
                obj_name = obj.text

                if 'Layer' in obj_name:
                    # print(obj_name)
                    node_properties.update({'Layer': [LAYER_CODE, obj.text]})

        # self.template.update({
        #     node.name: {'properties': node_properties,
        #                 'pos': node.pos
        #                 }
        # })
        self.template.update({
            node.name: {'properties': node_properties}})


# class SubContainer(BoxLayout):
# 	def __init__(self, **kwargs):
# 		super(SubContainer, self).__init__()
# 		self.orientation = 'vertical'


class ILayout(BoxLayout):
    def __init__(self, **kwargs):
        super(ILayout, self).__init__()
        self.orientation = 'vertical'

        self.add_widget(Interface())


class SubContainer1(BoxLayout):
    def __init__(self, **kwargs):
        super(SubContainer1, self).__init__()
        self.orientation = 'vertical'
        self.spacing = 5
        self.size_hint = (0.8, 1)
        self.state = 0

        self.tab_manager = TabManager(func=ILayout,
                                      default_name='New Model',
                                      _fkwargs={})
        # self.tab_manager.add_tab(func_name='New Model',
        #                          _fkwargs={})

        self.button_dict = {'Add Model': self.add_new_model}

        # `ui`: unimportant
        # self._ui_layout = BoxLayout(size_hint_y=0.06)
        # self._add_window_button = Button(size_hint_x=0.04,
        #                                  text='+')
        # self._add_window_button.bind(on_press=self._open_dropdown)

        # self._ui_layout.add_widget(Label(size_hint_x=0.96))
        # self._ui_layout.add_widget(self._add_window_button)

        # self.add_widget(MainBar())
        self.add_widget(self.tab_manager)
        # self.add_widget(self._ui_layout)

    # self.add_widget(SIToolBar(size_hint_y=0.1))

    def _open_dropdown(self, obj):
        overlay = get_obj(self, '_container').request_obj('Overlay')
        # overlay = self.parent.parent.parent.parent

        if self.state == 0:
            for i, key in enumerate(sorted(self.button_dict.keys())):
                button = Button(size_hint=(0.14, 0.0485),
                                pos=(obj.pos[0] - obj.width * 4.5,
                                     obj.pos[1] + i * 36),
                                text=key
                                )
                button.bind(on_press=self.button_dict[key])
                overlay.add_widget(button)

            self.state = 1

        elif self.state == 1:
            for children in overlay.children:
                if type(children) == Button:
                    overlay.remove_widget(children)

            self.state = 0

        return True

    def add_new_model(self, obj):
        self.tab_manager.add_tab(func_name='New Model',
                                 _fkwargs={})


class SubContainer2(BoxLayout):
    def __init__(self, **kwargs):
        super(SubContainer2, self).__init__()
        self.orientation = 'vertical'
        self.spacing = 10
        self.size_hint = (0.2, 1)

        self.sub_layout = BoxLayout(spacing=5,
                                    orientation='vertical',
                                    size_hint_y=0.5)

        # Update initial BaseInputForm for every BaseForms
        self.interface_toolbar = IToolBar()

        self.add_widget(self.sub_layout)
        self.add_widget(self.interface_toolbar)

        self.sub_layout.add_widget(ComponentPanel())


# self.sub_layout.add_widget(CreateBlock())


class Container(BoxLayout, Widget):
    def __init__(self, **kwargs):
        super(Container, self).__init__()
        self.orientation = 'vertical'
        self.spacing = 10

        # self.overlay = FloatLayout()

        self.main_sub_layout = BoxLayout(orientation='vertical',
                                         spacing=10)

        self.sub_layout = BoxLayout(orientation='horizontal',
                                    spacing=10,
                                    padding=10)

        self.sub_layout.add_widget(SubContainer1())
        self.sub_layout.add_widget(SubContainer2())

        self.tool_bar = CustomActionBar()
        # self.tool_bar = ActionBar()
        # self.action_view = ActionView()
        # self.action_view.add_widget(ActionPrevious())
        # self.action_view.add_widget(ActionButton())
        # self.action_view.add_widget(ActionButton())
        # self.action_view.add_widget(ActionButton())
        # self.tool_bar.add_widget(self.action_view)

        self.main_sub_layout.add_widget(self.tool_bar)
        self.main_sub_layout.add_widget(self.sub_layout)

        self.add_widget(self.main_sub_layout)

        self.bind(on_touch_up=self.open_right_click_menu)

    def open_right_click_menu(self, obj, touch):
        if touch.button == 'right':
            pass
