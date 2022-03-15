from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.widget import WidgetException

from utility.utils import get_obj


class RightClickMenu(BoxLayout):
    def __init__(self, funcs=None, button_width=120, button_height=40,
                 menu_height=50, **kwargs):
        super(RightClickMenu, self).__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (button_width, menu_height)
        self.orientation = 'vertical'

        self.button_width = button_width
        self.button_height = button_height
        self.funcs = funcs
        self.map_funcs_to_butt()

    def map_funcs_to_butt(self):
        for func_name in self.funcs.keys():
            button = Button(text=func_name,
                            size_hint=(None, None),
                            size=(self.button_width,
                                  self.button_height))
            button.bind(on_press=lambda obj: self.funcs[func_name]())
            self.add_widget(button)

        # self.pos_hint = kwargs.get('pos_hint')
        # self.size_hint = kwargs.get('size_hint')
        # self.size = kwargs.get('size')
        #
        # if func_list is None:
        #     func_list = {}
        #
        # self.func_list = func_list
        #
        # self.buttons_container = BoxLayout()
        # self.content = self.buttons_container

        # self.bind(on_touch_move=self.remove_toolbar)

        # self.add_buttons()

    # def add_buttons(self):
    #     for key in self.func_list.keys():
    #         button = Button(text=key,
    #                         size_hint=(1, 0.1))
    #         button.bind(on_release=self.func_list[key])
    #         self.buttons_container.add_widget(button)
