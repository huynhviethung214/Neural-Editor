from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.lang import Builder


class _Settings(GridLayout):
	pass


class app(App):
	def build(self):
		return Builder.load_file('settings_template.kv')


if __name__ == '__main__':
