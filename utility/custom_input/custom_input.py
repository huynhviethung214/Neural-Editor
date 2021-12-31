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

	def __init__(self, max_length=9, filter='str', hint_text='', font_size=16, **kwargs):
		super(CustomTextInput, self).__init__(**kwargs)
		self.max_length = max_length
		self.filter = filter
		self.hint_text = hint_text
		self.font_size = font_size

	def insert_text(self, substring, from_undo=False):
		if self.filter == 'int' or self.filter == 'float':
			if 0 < len(self.text) + 1 <= self.max_length:
				return super(CustomTextInput, self).insert_text(substring, from_undo)

		elif self.filter == 'str':
			if 0 < len(self.text) + 1 <= self.max_length:
				return super(CustomTextInput, self).insert_text(substring, from_undo)

