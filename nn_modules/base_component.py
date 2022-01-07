import json

from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.treeview import TreeViewLabel
from utility.utils import get_obj
from nn_modules.code_names import *
from utility.rightclick_toolbar.rightclick_toolbar import RightClickMenu


class Component(TreeViewLabel):
    def __init__(self, **kwargs):
        super(Component, self).__init__()
        # Template for custom list of functions
        self.toolbar_funcs = None

    def to_overlay(self, overlay, touch):
        return overlay.to_local(*self.to_window(*touch.pos))

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            interface = get_obj(self, 'InterfaceTabManager').current_tab.content.children[-1]

            if touch.button == 'left':
                interface._node = self.attachment
                interface._state = 1

        return True
