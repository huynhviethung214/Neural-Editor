# from math import floor
# from threading import Thread
# from time import sleep

# import torch
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.progressbar import ProgressBar
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App

# from nn_modules.node import Node
# from utility.base_form.baseform import BaseForm
from training_manager.training_manager import TrainingManager
from utility.utils import Sorter, get_obj, Net
from settings.config import configs
from Net.Net import Net

# device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')


class CheckpointButton(BoxLayout):
    def __init__(self, interface=None, **kwargs):
        super(CheckpointButton, self).__init__()


class IndicatorLabel(Label):
    def __init__(self, **kwargs):
        super(IndicatorLabel, self).__init__()

    def update(self, obj, val):
        self.font_size = (self.parent.width * 0.3,
                          self.parent.height * 0.3)


class _ProgressBar(ProgressBar):
    pass


class TrainButton(Button):
    def __init__(self, **kwargs):
        super(TrainButton, self).__init__()
        self.bind(on_press=self.train)
        self.sorter = Sorter()
        self.is_training = False
        self.model = None

        self.app = App.get_running_app()
        self.training_manager = self.app.training_manager

    def train(self, obj):
        interface = get_obj(self, 'Interface')

        try:
            if not self.is_training:
                # print('Training')
                self.model = Net(interface=interface).to(configs['device']['id'])
                self.training_manager.add_job(self.model, obj=self)
                self.text = 'X'
                self.is_training = True
            else:
                # print('Break Current Process')
                self.training_manager.end_task = True
                self.is_training = False
                self.text = '>'

        except ValueError as e:
            raise e
        return True
