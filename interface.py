import kivy
from kivy.app import runTouchApp
kivy.require('1.10.1')

from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.stencilview import StencilView
from kivy.uix.treeview import TreeViewLabel, TreeView
from kivy.lang import Builder
from kivy.app import App
from functools import partial
from node import Node


class Component(TreeViewLabel):
	def __init__(self, _name='Component', _attachment=Node, **kwargs):
		super(Component, self).__init__()
		self._attachment = _attachment
		self.text = _name

	def on_touch_move(self, touch):
		if self.collide_point(*touch.pos):
			Interface._node = self._attachment
			Interface._state = 1
		return True


class ComponentPanel(TreeView, Widget):
	def __init__(self, **kwargs):
		super(ComponentPanel, self).__init__()
		self.root_options = {'text': 'Component Panel'}
		self.add_node(Component())
		self.add_node(Component())


class ToolBar(BoxLayout, Widget):
	pass


class Interface(BoxLayout, StencilView, Widget):
	_node = None
	_state = 0

	def __init__(self, **kwargs):
		super(Interface, self).__init__()
		self.bind(on_touch_move=self.is_validate)
		self.bind(on_touch_up=partial(self._add_node, _self=self))

	def is_validate(self, obj, touch):
		if self.collide_point(*touch.pos):
			self.children[0].do_translation = True
		else:
			self.children[0].do_translation = False
		return True

	@classmethod
	def _add_node(cls, obj, touch, _self):
		if cls._state == 1 and _self.collide_point(*touch.pos):
			pos = _self.children[0].to_local(*touch.pos)
			node = cls._node(spos=pos)

			_self.children[0].add_widget(node)
			cls._node = None
			cls._state = 0
		else:
			cls._node = None
			cls._state = 0
		return True


class SubContainer(BoxLayout, Widget):
	pass

class Container(BoxLayout, Widget):
	pass


class _app(App):
	def build(self):
		return Builder.load_file('_template.kv')
	

if __name__ == '__main__':
	# Builder.load_file('_template.kv')
	# runTouchApp(_Interface())
	_app().run()
