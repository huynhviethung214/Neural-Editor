from kivy.uix.treeview import TreeViewLabel
from node import Node
from nn_nodes import LinearNode


class Component(TreeViewLabel):
	def __init__(self, _type='Component', _attachment=Node, interface=None, **kwargs):
		super(Component, self).__init__()
		self.add_properties()
		self.interface = interface

	def add_properties(self):
		pass

	def on_touch_down(self, touch):
		if self.collide_point(*touch.pos):
			self.interface._node = self._attachment
			self.interface._state = 1
		return True


class Linear(Component):
	def add_properties(self):
		self._attachment = LinearNode
		self.text = 'Linear'


class DataProcessor(Component):
	def add_properties(self):
		self._attachment = DataProcessorNode
		self.text = 'Data Processor'