from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.app import runTouchApp
from kivy.core.window import Window


class BaseWidget(BoxLayout, Widget):
	def __init__(self, dtype=None, dval=None, values=[], **kwargs):
		super(BaseWidget, self).__init__()
		self.size_hint = (1, 0.3)
		self.orientation = 'horizontal'

	def add_label(self, name):
		self.label = Label(text=name,
						font_size=15,
						size_hint_x=0.3,
						halign='center',
						valign='center')
		self.add_widget(self.label)


class BaseInputForm(BaseWidget):
	def __init__(self, **kwargs):
		super(BaseInputForm, self).__init__()
		self.name = kwargs.get('name')
		self.value = kwargs.get('dval')
		self.dtype = kwargs.get('dtype')

		self.input = TextInput(text=str(self.value),
								size_hint_x=0.6,
								multiline=False)

		self.add_label(self.name)
		self.add_widget(self.input)

	# def bind(self, func):
	# 	self.input.bind(text=partial(func, value=self.dtype(self.values)))


class BaseListForm(BaseWidget):
	def __init__(self, **kwargs):
		super(BaseListForm, self).__init__()
		self.name = kwargs.get('name')
		self.value = kwargs.get('dval')
		self.values = tuple(kwargs.get('values'))
		self.dtype = kwargs.get('dtype')

		self.input = Spinner(text=str(self.value),
							size_hint_x=0.6,
							values=self.values,
							sync_height=True)

		# self.input.bind(text=lambda obj, text: setattr(self, 'value',
		# 											self.dtype(self.input.text)))

		self.add_label(self.name)
		self.add_widget(self.input)

	# def bind(self, func):
	# 	self.input.bind(text=partial(func, value=self.values))


class BaseTensorForm(BaseWidget):
	def __init__(self, dname='None', **kwargs):
		super(BaseTensorForm, self).__init__()
		self.input = Button(text='Add',
							size_hint=(0.8, 0.7))

		self.add_label(self.dname)
		self.add_widget(self.input)


# runTouchApp(BaseListForm(dtype=bool, dval=1, dname='bool', values=['1', '0']))
# runTouchApp(BaseInputForm(dtype=bool, dval=1, dname='bool', values=[]))
# runTouchApp(BaseTensorForm(dname='List'))