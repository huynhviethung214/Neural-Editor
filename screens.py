from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.app import runTouchApp
from interface import Container
from kivy.app import App
from kivy.lang.builder import Builder
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget


class SettingScreen(Screen):
	pass


class InteractiveScreen(Screen):
	pass


class Manager(ScreenManager):
	pass


class ToolPanel(BoxLayout):
	pass


class _Container(BoxLayout):
	pass


class _app(App):
	def build(self):
		return Builder.load_file('screens_template.kv')


if __name__ == '__main__':
	_app().run()