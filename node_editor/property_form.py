from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner

from nn_modules.code_names import *
from utility.custom_input.custom_input import CustomTextInput


class PropertyForm(BoxLayout):
    def __init__(self, **kwargs):
        super(PropertyForm, self).__init__()
        self.size_hint = (0.9, 1)
        self.spacing = 4
        self.property = {'dtype': INT_CODE,
                         'property_name': None,
                         'default_value': None}

        self.str_to_type = {'int': INT_CODE,
                            'string': STR_CODE,
                            'bool': BOOL_CODE,
                            'float': FLOAT_CODE,
                            'matrix': MATRIX_CODE}

        self.datatype_list = Spinner(values=('int',
                                             'string',
                                             'bool',
                                             'float',
                                             'matrix'),
                                     size_hint=(0.2, 1),
                                     text='int',
                                     sync_height=True)
        self.datatype_list.bind(text=self.set_datatype)

        self.property_name = CustomTextInput(size_hint=(0.6, 1),
                                             max_length=20)
        self.property_name.bind(text=self.set_property_name)

        self.default_value = CustomTextInput(size_hint=(0.2, 1),
                                             max_length=20)
        self.default_value.bind(text=self.set_default_value)

        self.add_widget(self.property_name)
        self.add_widget(self.default_value)
        self.add_widget(self.datatype_list)

    def set_datatype(self, obj, value):
        self.property['dtype'] = self.str_to_type[value]

    def set_property_name(self, obj, value):
        self.property['property_name'] = value

    def set_default_value(self, obj, value):
        if self.property['property_name'] == INT_CODE:
            value = int(value)

        elif self.property['property_name'] == BOOL_CODE:
            value = [True if value == 'True' else False][0]

        self.property['default_value'] = value
