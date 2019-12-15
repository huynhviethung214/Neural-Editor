from functools import partial
from kivy.uix.spinner import Spinner
from kivy.app import runTouchApp


class MPDropDown(Spinner):
	def __init__(self, **kwargs):
		super(MPDropDown, self).__init__()

runTouchApp(MPDropDown())