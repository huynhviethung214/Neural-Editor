from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.spinner import Spinner
from .base_properties import BaseListForm, BaseInputForm
from functools import partial


class BaseForm(GridLayout, Widget):
    _children = []

    def __init__(self, **kwargs):
        super(BaseForm, self).__init__()
        self.do_scroll_x = False
        self.do_scroll_y = True
        self.padding = 10
        self.cols = 1
        self.rows = 2

        self.func_list = []
        self.func_names = []
        self.c_func = None

        self.sub_layout = GridLayout(size_hint=(1, None),
                                     spacing=5,
                                     height=400)
        self.sub_layout.row_force_default = True
        self.sub_layout.row_default_height = 30
        self.sub_layout.cols = 1

    def build_subform(self):
        self.sub_layout.clear_widgets()
        props = self.c_func.prop_dict.keys()
        prop_dict = self.c_func.prop_dict
        self.sub_layout.rows = len(props)

        for prop in props:
            if type(prop_dict[prop]) == int or type(prop_dict[prop]) == float or type(prop_dict[prop]) == str:
                self.add_input_form(prop, prop_dict[prop], type(prop_dict[prop]))

            elif type(prop_dict[prop]) == (list or dict or 'Tensor'):
                pass

            elif type(prop_dict[prop]) == bool:
                self.add_list_form(prop, prop_dict[prop], bool, ['False', 'True'])

    def add_drop_down_list(self, source=None, _filter=None, is_spinner=1):
        for f in dir(source):
            if '___' in f:
                src_name = str(source).split(' ')[1]
                src_name = src_name.split("'")[1]

                module = __import__(src_name, fromlist=[f])
                _class = getattr(module, f)
                
                # print(_class.__str__())

                self.func_list.append(_class)
                self.func_names.append(_class.__str__())
        
        if is_spinner:
            spinner = Spinner(text=self.func_names[0],
                              values=tuple(self.func_names),
                              sync_height=True,
                              size_hint=(1, None),
                              height=40)
            spinner.bind(text=self.choose_func)
            self.add_widget(spinner)

        self.c_func = self.func_list[0]
        self.build_subform()

        self.add_widget(self.sub_layout)

    # Add CustomTextInput
    def add_input_form(self, name, dval, dtype):
        input_form = BaseInputForm(dtype=dtype,
                                   dval=dval,
                                   name=name)
        self._bind(input_form, dval, name, dtype)
        self.sub_layout.add_widget(input_form)

    def add_list_form(self, name, dval, dtype, values):
        list_form = BaseListForm(dtype=dtype,
                                 dval=dval,
                                 name=name,
                                 values=values)
        self._bind(list_form, dval, name, dtype)
        self.sub_layout.add_widget(list_form)

    def choose_func(self, obj, text):
        for func in self.func_list:
            if func.__str__() == text:
                self.c_func = func
                break

        self.build_subform()

    def _bind(self, obj, value, name, dtype):
        obj.children[0].bind(text=partial(self.set_value, name=name, dtype=dtype))

    def set_value(self, obj, value, name, dtype):
        try:
            self.c_func.prop_dict[name] = dtype(value)

        except Exception:
            pass

    def get_alg(self, params=None, _type=0):
        return self.c_func.algorithm(params=params, _type=_type)
