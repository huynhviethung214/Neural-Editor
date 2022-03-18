import json

from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.treeview import TreeViewLabel
from utility.utils import get_obj
from nn_modules.code_names import *
from utility.rightclick_toolbar.rightclick_toolbar import RightClickMenu


class Component(TreeViewLabel):
    def __init__(self, tree_view, **kwargs):
        super(Component, self).__init__()
        # Template for custom list of functions
        self.toolbar_funcs = None
        self.node_funcs = {
            'Delete Node': self.delete_node
        }
        self.tree_view = tree_view

    def to_overlay(self, overlay, touch):
        return overlay.to_local(*self.to_window(*touch.pos))

    def delete_node(self):
        nodes = json.load(open('./nn_modules/nn_nodes.json'))
        nodes.pop(self.tree_view.selected_node.text)

        open('./nn_modules/nn_nodes.json', 'w').write(
            json.dumps(nodes,
                       sort_keys=True,
                       indent=4)
        )
        self.tree_view.remove_node(self.tree_view.selected_node)

    def open_node_rightclick_menu(self, obj, touch):
        overlay = get_obj(self, 'Overlay')
        overlay.clear_menu()

        if touch.button == 'right' and self.collide_point(*touch.pos):
            overlay.open_menu(
                RightClickMenu(funcs=self.node_funcs,
                               pos=overlay.to_overlay_coord(touch,
                                                            self.tree_view.selected_node)
                               )
            )

        return True

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            overlay = get_obj(self, 'Overlay')
            overlay.clear_menu()

            if touch.button == 'left':
                interface = get_obj(self, 'InterfaceTabManager').current_tab.content.children[-1]
                interface._node = self.attachment
                interface._state = 1

            elif touch.button == 'right':
                overlay.open_menu(
                    RightClickMenu(funcs=self.node_funcs,
                                   pos=overlay.to_overlay_coord(touch,
                                                                self.tree_view.selected_node)
                                   )
                )

        return True
