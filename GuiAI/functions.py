from node import Node
from processors import ImageProcessor


class Input(Node):
	def add_components(self):
		self.set_id(_type='Input', _self=self)
		self.add_id()
		self.add_val_input('dataset', str)
		self.add_val_input('width', float)
		self.add_val_input('height', float)
		self.add_val_input('split', float)
		self.add_val_input('z', float)
		self.add_list_data('shuffle', [False, True])

	def algorithm(self):
		pass

	def set_val(self, obj, val, name):
		try:
			if val != '':
				if self.properties[name][0] == int:
					self.processor.properties[name] = int(val)

				elif self.properties[name][0] == float:
					self.processor.properties[name] = float(val)

				elif self.properties[name][0] == str:
					self.processor.properties[name] = val

		except Exception:
			obj.text = ''

	def set_bool(self, ins, name, val, button, tf_list):
		tf_list.select(button.text)
		self.processor.properties[name] = val

	def add_custom_properties(self):
		self.processor = ImageProcessor()
		self._type = 3
