# from math import floor
# from threading import Thread
# from time import sleep

# import torch
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App

# from nn_modules.node import Node
# from utility.base_form.baseform import BaseForm
from message_box.message_box import MessageBox
from training_manager.training_manager import TrainingManager
from utility.utils import get_obj
from settings.config import configs
from Net.Net import Net


# device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')


class CheckpointButton(BoxLayout):
    def __init__(self, **kwargs):
        super(CheckpointButton, self).__init__(**kwargs)
        self.app = App.get_running_app()
        self.training_manager = self.app.training_manager

        self.checkbox = self.children[0]
        self.checkbox.bind(active=lambda obj, val: setattr(self.training_manager, 'save_checkpoint', val))


class ModeLabel(Label):
    def __init__(self, **kwargs):
        super(ModeLabel, self).__init__(**kwargs)
        self.text = 'Mode: '


class TrainedModelLabel(Label):
    def __init__(self, **kwargs):
        super(TrainedModelLabel, self).__init__(**kwargs)
        self.text = 'Model: '

    def update_text(self, model_name):
        self.text += model_name


class ProgressIndicator(Label):
    def __init__(self, **kwargs):
        super(ProgressIndicator, self).__init__(**kwargs)
        self.text = '0% / 0%'


class TrainButton(Button):
    def __init__(self, **kwargs):
        super(TrainButton, self).__init__()
        self.bind(on_press=self.train)
        self.is_training = False

        self.app = App.get_running_app()
        self.training_manager = self.app.training_manager

    # Converting str_mapped_path to mapped_path (str list: [`Node 0`, `Node 1`] -> obj list: [Node 0, Node 1])
    @staticmethod
    def to_mapped_path(interface):
        mapped_path = []
        str_mapped_path = interface.str_mapped_path

        for node_name in str_mapped_path:
            for node in interface.nodes():
                if node.name == node_name:
                    mapped_path.append(node)
                    break

        # print(mapped_path)
        return mapped_path

    def train(self, obj):
        interface = get_obj(self, 'Interface')

        try:
            if not self.is_training:
                # print('Training')
                model = Net(nodes=interface.nodes,
                            interface=interface,
                            mapped_path=self.to_mapped_path(interface)).to(configs['device']['id'])
                # print(self.model)
                self.training_manager.setup_train(model,
                                                  obj=self,
                                                  interface=interface)
                if interface.model_name:
                    self.training_manager.model_name = interface.model_name

                elif not interface.model_name:
                    self.training_manager.model_name = 'Unknown'

                self.text = 'X'
                self.is_training = True
            else:
                # print('Break Current Process')
                self.training_manager.end_task = True
                self.text = '>'
                self.is_training = False

        except ValueError as e:
            MessageBox(message_type='Failed To Queue Model',
                       message=str(e)).open()
        return True
