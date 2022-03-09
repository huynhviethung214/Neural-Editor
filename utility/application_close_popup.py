import json
import sys
from functools import partial

from kivy.base import stopTouchApp
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.app import App

from utility.utils import get_obj


class ApplicationClosePopup(Popup):
    def __init__(self, **kwargs):
        super(ApplicationClosePopup, self).__init__()
        self.size_hint = (0.4, 0.2)
        self.title = 'Notification'

        self.layout = BoxLayout(orientation='vertical',
                                spacing=2)
        self.sub_layout = BoxLayout(size_hint=(1, 0.4))

        self.app = kwargs.get('app')
        self.container = kwargs.get('container')

        accept_button = Button(text='Save', size_hint=(0.33, 1))
        deny_button = Button(text='No', size_hint=(0.33, 1))
        cancel_button = Button(text='Cancel', size_hint=(0.34, 1))

        self.sub_layout.add_widget(accept_button)
        self.sub_layout.add_widget(deny_button)
        self.sub_layout.add_widget(cancel_button)

        self.layout.add_widget(Label(text='This model has been modified, save changes?',
                                     size_hint=(1, 0.6)))
        self.layout.add_widget(self.sub_layout)
        self.add_widget(self.layout)

        accept_button.bind(on_release=self.save_model)
        deny_button.bind(on_release=self.close_app)
        cancel_button.bind(on_release=self.cancel)

    # TODO: FIX `saved_model` function
    def save_model(self, obj):
        custom_action_bar = get_obj(self.container, 'CustomActionBar')
        custom_action_bar.save_model(None)
        # tab_manager = [widget for widget in self.container.walk(loopback=True) if 'TabManager' in str(widget)][0]
        # interface = tab_manager.current_tab.content.children[-1]
        # model = interface.m_list
        #
        # sorter = Sorter()
        # sorted_model = sorter.sort(model)
        #
        # interface._template.update({'links': [block for block in sorted_model.blocks.keys()],
        #                             'beziers': [bezier.points for bezier in interface.beziers]})
        #
        # with open('models\\' + interface.model_name + '.json', 'w') as f:
        #     json.dump(interface._template,
        #               f,
        #               sort_keys=True,
        #               indent=4)
        self.app.stop()

    def close_app(self, obj):
        Window.close()
        sys.exit(0)

    def cancel(self, obj):
        self.dismiss()
