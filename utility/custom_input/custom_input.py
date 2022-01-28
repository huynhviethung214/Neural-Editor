from kivy.uix.textinput import TextInput


class CustomTextInput(TextInput):
	# @staticmethod
	# def update_padding(obj, *args):
	# 	text_width = obj._get_text_width(
	# 		obj.text,
	# 		obj.tab_width,
	# 		obj._label_cached
	# 	)
	# 	obj.padding_x = (obj.width - text_width) / 2

	def __init__(self, max_length=9, hint_text='', filter='str', **kwargs):
		super(CustomTextInput, self).__init__(**kwargs)
		self.max_length = max_length
		self.hint_text = hint_text
		self.filter = filter

		self.multiline = False
		self.alphabet = 'abcdefghijklmnopqrstuvwxyz'

		self.bind(on_text_validate=self.on_enter)

	def is_in_alphabet(self, string):
		for character in string:
			if character in self.alphabet or character in self.alphabet.upper():
				return 1
		return 0

	def on_enter(self, obj):
		value = str(self.text)
		try:
			if not self.is_in_alphabet(value):
				self.text = str(eval(value))

		except Exception as e:
			self.text = ''

	def insert_text(self, substring, from_undo=False):
		if self.filter == 'int' or self.filter == 'float':
			if 0 < len(self.text) + 1 <= self.max_length:
				return super(CustomTextInput, self).insert_text(substring, from_undo)

		elif self.filter == 'str':
			if 0 < len(self.text) + 1 <= self.max_length:
				return super(CustomTextInput, self).insert_text(substring, from_undo)

