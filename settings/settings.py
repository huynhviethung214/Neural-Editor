import GPUtil
import json
from os.path import exists

from kivy.uix.textinput import TextInput

from .config import configs
# from cpuinfo import get_cpu_info
# from importlib import reload

# import torch

from utility.base_form.base_properties import *
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout


# Setting format:
#   Device: `Something Something`


class ButtonForm(BoxLayout):
    def __init__(self, text, butt_name, **kwargs):
        super(ButtonForm, self).__init__()
        self.orientation = 'horizontal'

        self.add_widget(Label(text=text))
        self.add_widget(Button(text=butt_name))


class SettingsLayout(GridLayout):
    def __init__(self, **kwargs):
        super(SettingsLayout, self).__init__()
        self.cols = 1
        self.rows = 10
        self.row_force_default = True
        self.row_default_height = 40
        self.spacing = 6

        self.fpath = 'settings/settings.json'
        self.settings = configs.default_config

        apply_butt = Button(text='Save & Apply Settings')
        # Apply & save settings
        apply_butt.bind(on_press=self.apply_settings)

        # SELECT DEVICE TO TRAIN ON
        self.device_select_butt = BaseListForm(name='Select GPU',
                                               dval=configs.default_config['device']['name'],
                                               values=configs.devices)
        self.device_select_butt.input.bind(text=self.select_device)

        # WEIGHT'S FILEPATH
        self.weight_filepath = BaseInputForm(name='Weight\'s filepath',
                                             dval=configs.default_config['weight_path'],
                                             dtype=str,
                                             max_len=100)
        self.weight_filepath.input.bind(text=self.set_wfp)

        # MODEL'S FILEPATH
        self.models_fp = BaseInputForm(name='Model\'s filepath',
                                       dval=configs.default_config['models_path'],
                                       dtype=str,
                                       max_len=100)
        self.models_fp.input.bind(text=self.set_wfp)

        self.add_widget(self.device_select_butt)
        self.add_widget(self.weight_filepath)
        self.add_widget(self.models_fp)
        self.add_widget(apply_butt)

    def set_wfp(self, obj, text):
        self.settings['weight_path'] = text

    def select_device(self, obj, text):
        # print(text)
        self.settings['device']['name'] = text
        self.settings['device']['id'] = text.split(' ')[-1][1:-1]
        # print(self.settings)

    def apply_settings(self, obj):
        with open(self.fpath, 'w') as f:
            json.dump(self.settings,
                      f,
                      sort_keys=True,
                      indent=4)

        # print('Reload Configs')
        # Reload config.py & apply new settings
        configs.reload_config()
