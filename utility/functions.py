from nn_modules.node import Node
from utility.utils import _Flatten


class _FlattenLayer(Node):
	def add_components(self):
		self.set_id(_type='Flatten', _self=self)
		self.add_id()

	def algorithm(self):
		return _Flatten()
