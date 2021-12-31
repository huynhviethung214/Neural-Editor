from kivy.uix.boxlayout import BoxLayout
# from kivy.uix.label import Label
from kivy.uix.spinner import Spinner

from nn_modules.code_names import *
from utility.custom_input.custom_input import CustomTextInput


class NLForm(BoxLayout):
    def __init__(self, nl_type='input', **kwargs):
        super(NLForm, self).__init__()
        self.size_hint = (1, 1)
        self.spacing = 4

        self.property = {'type': nl_type,
                         'position': LEFT_CODE,
                         'n_links': 2}
        self.hint_text = kwargs.get('hint_text')

        self.str_to_type = {'left': LEFT_CODE,
                            'right': RIGHT_CODE,
                            'top': TOP_CODE,
                            'bottom': BOTTOM_CODE,
                            'input': NL_IN,
                            'output': NL_OUT}

        self.position = Spinner(values=('left',
                                        'right',
                                        'top',
                                        'bottom'),
                                size_hint=(0.4, 1),
                                text='left',
                                sync_height=True)
        self.position.bind(text=self.set_position)

        self.inputs = CustomTextInput(size_hint=(0.6, 1),
                                      filter='int',
                                      hint_text=self.hint_text)
        self.inputs.bind(text=self.set_n_links)

        # self.link_type = Spinner(values=('input',
        #                                  'output'),
        #                          size_hint=(0.4, 1),
        #                          text='input',
        #                          sync_height=True)
        # self.link_type.bind(text=self.set_type)

        # self.add_widget(self.link_type)
        self.add_widget(self.inputs)
        self.add_widget(self.position)

    def set_n_links(self, obj, value):
        if value != '':
            self.property['n_links'] = int(value)
            return True

    # def set_type(self, obj, value):
    #     if value != '':
    #         self.property['type'] = int(value)
    #         return True

    def set_position(self, obj, value):
        if value != '':
            _type = self.str_to_type[value]
            self.property['position'] = _type
            return True
