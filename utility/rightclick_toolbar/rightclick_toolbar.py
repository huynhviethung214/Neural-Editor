from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.widget import WidgetException

from utility.utils import get_obj


class RightClickMenu(Popup):
    def __init__(self, func_list=None, selected_node=None, **kwargs):
        super(RightClickMenu, self).__init__()
        self.pos_hint = kwargs.get('pos_hint')
        self.size_hint = kwargs.get('size_hint')
        self.size = kwargs.get('size')

        if func_list is None:
            func_list = {}

        self.func_list = func_list

        self.buttons_container = BoxLayout()
        self.content = self.buttons_container

        # self.bind(on_touch_move=self.remove_toolbar)

        self.add_buttons()

    def add_buttons(self):
        for key in self.func_list.keys():
            button = Button(text=key,
                            size_hint=(1, 0.1))
            button.bind(on_release=self.func_list[key])
            self.buttons_container.add_widget(button)

    def open_toolbar(self, touch):
        self.overlay.add_widget(self)

    def remove_toolbar(self, obj, touch):
        if self in self.overlay.children:
            self.overlay.remove_widget(self)
