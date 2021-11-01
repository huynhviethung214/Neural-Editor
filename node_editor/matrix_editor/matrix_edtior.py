from functools import partial

from kivy.app import runTouchApp, App
from kivy.clock import Clock
from kivy.graphics import Line
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.lang import Builder
from kivy.uix.widget import Widget


class T(TextInput):
    # max_length = 3

    def __init__(self, max_length=2, **kwargs):
        super(T, self).__init__(**kwargs)
        self.max_length = max_length
        # self.padding_x = 20
        # self.padding_y = 20
        # self.multiline = False
        # self.font_size = 10

        # with self.canvas:
        #     Line(rectangle=(self.x, self.y, self.width, self.height))

    def insert_text(self, substring, from_undo=False):
        if len(self.text) <= self.max_length:
            # Clock.schedule_once(lambda dt: super(T, self).insert_text(substring, from_undo), 1)
            return super(T, self).insert_text(substring, from_undo)


class MatrixEditor(BoxLayout):
    def __init__(self, **kwargs):
        super(MatrixEditor, self).__init__()
        self.size_hint = (0.3, 0.4)
        # self.auto_dismiss = False

        self.main_layout = BoxLayout(spacing=4,
                                     padding=5)

        # Sub-layout 1
        self.sub_layout1 = BoxLayout(orientation='vertical',
                                     spacing=4)
        self.grid_input_layout = BoxLayout(orientation='horizontal',
                                           size_hint=(1, 0.1),
                                           padding=4)

        self.cols_input = T(size_hint=(0.1, 1),
                            font_size=15)
        self.rows_input = T(size_hint=(0.1, 1),
                            font_size=15)

        self.rows_input.bind(text=self.grid_size_input)
        self.cols_input.bind(text=self.grid_size_input)

        # Grid Size Input
        self.grid_input_layout.add_widget(self.cols_input)
        self.grid_input_layout.add_widget(Label(text='x',
                                                size_hint=(0.1, 1)))
        self.grid_input_layout.add_widget(self.rows_input)
        self.grid_input_layout.add_widget(Widget(size_hint=(1, 1)))

        self.sub_layout1.add_widget(self.grid_input_layout)
        self.sub_layout1.add_widget(GridLayout())

        # Sub-layout 2
        self.sub_layout2 = BoxLayout(orientation='vertical',
                                     size_hint=(0.4, 1))
        self.sub_layout2.add_widget(Button(text='Data-type'))
        self.sub_layout2.add_widget(Button())
        self.sub_layout2.add_widget(Button())

        self.main_layout.add_widget(self.sub_layout1)
        self.main_layout.add_widget(self.sub_layout2)

        self.add_widget(self.main_layout)
        # Clock.schedule_interval(self.test, 1)

    def grid_size_input(self, obj, value):
        if value != '':
            if 1 <= int(value) <= 20:
                grid_layout = GridLayout()
                grid_layout.rows = int(value)
                grid_layout.cols = int(value)

                obj1 = [m for m in self.grid_input_layout.children if m != obj and type(m) == TextInput][0]
                # Clock.schedule_once(lambda dt: setattr(obj1, 'text', value), 1)
                obj1.text = value
                obj1.select(len(value), len(value))
                # print(obj1.text, value)
                self.test(int(value), grid_layout)
            else:
                self.cols_input.text = ''
                self.rows_input.text = ''
        else:
            self.clear_grid_layout()
            self.sub_layout1.add_widget(GridLayout())

            return True

    def clear_grid_layout(self):
        for children in self.sub_layout1.children:
            if type(children) == GridLayout:
                self.sub_layout1.remove_widget(children)

    def test(self, value, grid_layout):
        self.clear_grid_layout()

        for i in range(value ** 2):
            grid_layout.add_widget(T(font_size=10))

        # If rows/cols = 2 then increase the padding
        if value > 1:
            grid_layout.padding = (grid_layout.children[0].width * 3) / grid_layout.rows
        else:
            grid_layout.padding = self.width * 2 / 7
        grid_layout.spacing = 3
        self.sub_layout1.add_widget(grid_layout)


class app(App):
    def build(self):
        return Builder.load_file('matrix_editor.kv')


if __name__ == '__main__':
    app().run()
