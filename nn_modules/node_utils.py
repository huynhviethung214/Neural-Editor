from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner

from utility.custom_input.custom_input import CustomTextInput


class KernelInput(BoxLayout):
    def __init__(self, **kwargs):
        super(KernelInput, self).__init__()
        self.default_size = kwargs.get('default_size')
        self.size_hint = (0.6, 1)
        self.spacing = 4
        self.height = 25

        self.m = CustomTextInput(text=str(self.default_size[0]),
                                 font_size=12)
        self.n = CustomTextInput(text=str(self.default_size[1]),
                                 font_size=12)

        self.add_widget(self.m)
        self.add_widget(Label(text='x',
                              size_hint_x=0.2))
        self.add_widget(self.n)


class CustomSpinnerInput(BoxLayout):
    def __init__(self, c_height=None, default_halign='center', **kwargs):
        super(CustomSpinnerInput, self).__init__()
        self.size_hint = (1, 1)
        self.height = c_height
        self.spacing = 20
        self.height = 25

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


class CustomValueInput(BoxLayout):
    def __init__(self, default_halign='center', **kwargs):
        super(CustomValueInput, self).__init__()
        self.size_hint = (1, 1)
        self.spacing = 20
        self.height = 25

        self.label = Label(text=kwargs.get('name'),
                           halign=default_halign,
                           valign='middle',
                           width=100,
                           font_size=14,
                           text_size=(100, 35),
                           size_hint=(0.4, 1),
                           max_lines=1,
                           shorten=True,
                           shorten_from='right')
        self.input = CustomTextInput(font_size=12,
                                     width=90,
                                     size_hint=(0.6, 1),
                                     max_length=30)

        self.add_widget(self.label)
        self.add_widget(self.input)