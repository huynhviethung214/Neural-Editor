from kivy.uix.treeview import TreeViewLabel
from nn_modules.node import Node
from nn_modules.nn_nodes import LinearNode, _XConv2d
from ultility.functions import _FlattenLayer


class Component(TreeViewLabel):
	def __init__(self, _type='Component', _attachment=Node, interface=None, **kwargs):
		super(Component, self).__init__()
		self.add_properties()
		self.interface = interface

	def generate_obj(self):
		return type(str(self._attachment),
					(self._attachment,),
					{})

	def add_properties(self):
		pass

	def on_touch_down(self, touch):
		if self.collide_point(*touch.pos):
			self.interface._node = self.generate_obj()
			self.interface._state = 1
		return True


class Linear(Component):
	def add_properties(self):
		self._attachment = LinearNode
		self.text = 'Linear'


class XConv2d(Component):
	def add_properties(self):
		self._attachment = _XConv2d
		self.text = 'XConv2d'


# class ImageDataProcessor(Component):
# 	def add_properties(self):
# 		self._attachment = _ImageDataProcessor
# 		self.text = 'Image Processor'


class Flatten(Component):
	def add_properties(self):
		self._attachment = _FlattenLayer
		self.text = 'Flatten'
