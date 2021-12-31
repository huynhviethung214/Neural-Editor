from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.app import App
from kivy.lang.builder import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window

from graph.graph import Graphs
from training_manager.training_manager import TrainingManager
from utility.notification_popup import NotificationPopup
from i_modules.interface.interface import Container
from settings.settings import *
from editor_modules.scripting_interface import *
from kivy.config import Config

import kivy
import os
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"

from utility.rightclick_toolbar.rightclick_toolbar import RightClickMenu

kivy.require('2.0.0')

Config.set('kivy', 'exit_on_escape', '0')
Config.set('graphics', 'width', '1980')
Config.set('graphics', 'height', '1080')

# Config.set('graphics', 'position', 'custom')
# Config.set('graphics', 'left', 0)
# Config.set('graphics', 'top',  0)


class SettingScreen(Screen):
    pass


class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__()
    # client.assign_obj('main_screen', self)


class ScriptingScreen(Screen):
    pass


class GraphScreen(Screen):
    def __init__(self, **kwargs):
        super(GraphScreen, self).__init__(**kwargs)
        self.layout = BoxLayout()
        self.graph_tab_manager = TabManager(func=Graphs,
                                            default_name='New Graph',
                                            _fkwargs={},
                                            add_default_tab=False)

        self.layout.add_widget(self.graph_tab_manager)
        self.add_widget(self.layout)


class Manager(ScreenManager):
    pass


class ToolPanel(BoxLayout):
    pass


class Overlay(FloatLayout):
    def __init__(self, **kwargs):
        super(Overlay, self).__init__()
    #     self.bind(on_touch_down=self.clear)
    #
    # def clear(self, obj, touch):
    #     self.remove_toolbar()
    #
    # def remove_toolbar(self):
    #     for children in get_obj(self, 'Overlay').children:
    #         if type(children) == RightClickMenu:
    #             get_obj(self, 'Overlay').remove_widget(children)


class _Container(BoxLayout):
    def __init__(self, **kwargs):
        super(_Container, self).__init__()
        self.spacing = 4
        self.obj_dict = {}

        self.add_widget(Manager())
        self.add_widget(ToolPanel())

    def tree_hierarchy(self):
        for widget in self.walk(loopback=True):
            if 'Screen' in str(widget):
                self.obj_dict.update({str(widget): widget})
            else:
                name = str(widget).split(' ')[0].split('.')[-1]
                self.obj_dict.update({name.lower(): widget})

    def request_obj(self, w_name):
        return self.obj_dict[w_name.lower()]


class _app(App):
    def build(self):
        self.set_properties()
        self.binding()

        self.training_manager = TrainingManager()

        self.main_container = _Container()
        self.main_container.tree_hierarchy()

        Window.size = (1980, 1080)
        Window.maximize()

        return self.main_container

    def binding(self):
        Window.bind(on_request_close=self.on_app_close)

    def set_properties(self):
        self.title = 'Neural Editor'

    def on_app_close(self, *args):
        popup = NotificationPopup(obj=self,
                                  container=self.main_container)
        popup.open()

        return True


if __name__ == '__main__':
    Builder.load_file('screens_template.kv')
    _app().run()
