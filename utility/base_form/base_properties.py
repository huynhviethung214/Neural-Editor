from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner

from utility.custom_input.custom_input import CustomTextInput


class BaseWidget(BoxLayout, Widget):
    def __init__(self, values=None, **kwargs):
        super(BaseWidget, self).__init__()

        if values is None:
            values = []

        self.size_hint = (1, 0.05)
        self.orientation = 'horizontal'

    def add_label(self, name):
        self.label = Label(text=name,
                           font_size=15,
                           size_hint_x=0.5,
                           halign='center',
                           valign='center')
        self.add_widget(self.label)


class BaseInputForm(BaseWidget):
    def __init__(self, name: str, dval='', dtype=str, max_len=9, **kwargs):
        super(BaseInputForm, self).__init__()
        self.name = name
        self.value = dval
        self.dtype = dtype

        self.input = CustomTextInput(text='',
                                     size_hint_x=0.4,
                                     multiline=False,
                                     max_length=max_len)
        # self.input.bind(text=self.to_datatype)

        self.add_label(self.name)
        self.add_widget(self.input)
        
        Clock.schedule_once(self.update_text, 0)
        # Clock.schedule_once(lambda *args: setattr(self, 'input.text', str(self.value)), 0)

    def update_text(self, *args):
        self.input.text = str(self.value)


class BaseListForm(BaseWidget):
    def __init__(self, name: str, dval=None, values=None, **kwargs):
        super(BaseListForm, self).__init__()
        self.name = name
        self.value = dval
        self.values = values
        # self.dtype = kwargs.get('dtype')

        self.input = Spinner(text=str(self.value),
                             size_hint_x=0.4,
                             values=self.values,
                             sync_height=True)

        self.add_label(self.name)
        self.add_widget(self.input)


class BaseTensorForm(BaseWidget):
    def __init__(self, dname='None', **kwargs):
        super(BaseTensorForm, self).__init__()
        self.input = Button(text='Add',
                            size_hint=(0.8, 0.7))

        self.add_label(self.dname)
        self.add_widget(self.input)
