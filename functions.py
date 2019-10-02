from node import Node
from processors import _ImageProcessor
from utils import _Flatten


# class _ImageDataProcessor(Node):
# 	def add_components(self):
# 		self.set_id(_type='Image Processor', _self=self)
# 		self.add_id()
# 		self.add_drop_down_list()
# 		self.add_val_input('dataset', str)
# 		self.add_val_input('width', int)
# 		self.add_val_input('height', int)
# 		self.add_val_input('split', float)
# 		self.add_val_input('z', int)
# 		self.add_list_data('shuffle', [True, False])

# 	def algorithm(self):
# 		pass

# 	def set_val(self, obj, val):
# 		try:
# 			if val != '':
# 				if self.properties[name][0] == int:
# 					self.processor.properties[name] = int(val)

# 				elif self.properties[name][0] == float:
# 					self.processor.properties[name] = float(val)

# 				elif self.properties[name][0] == str:
# 					self.processor.properties[name] = val

# 		except Exception:
# 			obj.text = ''

# 	def set_bool(self, ins, name, val, button, tf_list):
# 		tf_list.select(button.text)
# 		self.processor.properties[name] = val

# 	def add_custom_properties(self):
# 		self.processor = _ImageProcessor()
# 		# print(self._type)


class _FlattenLayer(Node):
	def add_components(self):
		self.set_id(_type='Flatten', _self=self)
		self.add_id()

	def algorithm(self):
		return _Flatten()
