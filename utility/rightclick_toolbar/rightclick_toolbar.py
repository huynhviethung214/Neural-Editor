from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.widget import WidgetException

from utility.utils import get_obj


class RightClickToolBar(BoxLayout):
    def __init__(self, **kwargs):
        super(RightClickToolBar, self).__init__()
        self.func_list = kwargs.get('func_list')
        self.obj = kwargs.get('obj')
        self.interface = kwargs.get('interface')

        self.size_hint = (0.1, 0.2)

        self.overlay = get_obj(self.interface, 'OverLay')
        # self.bind(on_touch_up=self.open_toolbar)
        self.bind(on_touch_move=self.remove_toolbar)

    def add_buttons(self):
        for key in self.func_list.keys():
            button = Button(text=key,
                            size_hint=(1, 0.2))
            button.bind(on_release=self.func_list[key])
            self.add_widget(button)

    def open_toolbar(self, obj, touch):
        # pos = self.to_local(*touch.pos)
        # print(self)
        # print(obj)
        # print(obj.collide_point(*touch.pos))
        if touch.button == 'right' and obj.collide_point(*touch.pos):
            if self not in self.overlay.children:
                self.overlay.add_widget(self)
                self.pos = self.to_local(*obj.to_window(*touch.pos))
            else:
                self.pos = self.to_local(*obj.to_window(*touch.pos))

    def remove_toolbar(self, obj, touch):
        if self in self.overlay.children:
            self.overlay.remove_widget(self)
