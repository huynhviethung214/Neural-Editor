import kivy
from kivy.app import runTouchApp
kivy.require('1.10.1')

from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.stencilview import StencilView
from kivy.uix.treeview import TreeViewLabel, TreeView
from kivy.graphics import Bezier
from kivy.lang import Builder
from kivy.app import App
from functools import partial
from kivy.clock import Clock
from node import Node, NodeLink


class Component(TreeViewLabel):
	def __init__(self, _name='Component', _attachment=Node, **kwargs):
		super(Component, self).__init__()
		self._attachment = _attachment
		self.text = _name

	def on_touch_down(self, touch):
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


class Interface(StencilView, Widget):
	_node = None
	_state = 0
	_spos = (0, 0)

	def __init__(self, **kwargs):
		super(Interface, self).__init__()
		self.ori = (0, 0)
		self.end = (0, 0)

		self.p_node_link = None
		self.is_drawing = None
		self.links = []
		self.ind = []

		self.bind(on_touch_up=partial(self._add_node, _self=self))
		self.bind(on_touch_move=self.is_validate)
		self.bind(on_touch_move=self.unbind)

		self.bind(on_touch_move=self.draw_link)
		self.bind(on_touch_move=self.update_canvas)

		self.bind(on_touch_down=self.node_down)
		self.bind(on_touch_up=self.node_up)

	def _check_nl_collision(self, touch):
		for node in self.children[0].children:
			for node_link in node.children[0].children:
				if type(node_link) == NodeLink:
					pos = node_link.to_widget(*touch.pos)
					if node_link.collide_point(*pos):
						return True, node, node_link
		return False, None, None

	def unbind(self, obj, touch):
		_, node, node_link = self._check_nl_collision(touch=touch)
		if node_link != None:
			if self.is_drawing and node_link.target != None:
				for info in self.links:
					if node_link in info and node_link.target in info:
						try:
							self.ind.remove(info[-1])
							self.clear_canvas()
							node.unbind(node_link, node_link._type)

							node_link.target.t_pos = None
							node_link.target.target = None

							node_link.target = None
							node_link.t_pos = None

						except ValueError:
							pass
			return True

	def node_up(self, obj, touch):
		valid, node, node_link = self._check_nl_collision(touch=touch)
		if valid:
			node._bind(_self=node,
					   state=2,
					   nav=node_link._type)
			_pos = self.get_pos(node_link, node_link.pos)

			node_link.c_pos = _pos
			node_link.target = self.p_node_link
			node_link.t_pos = self.p_node_link.c_pos

			self.p_node_link.t_pos = _pos
			self.p_node_link.target = node_link
			
			_pos = (_pos[0] + 5, _pos[1] + 5)
			bezier = self.draw(self.ori, _pos)
			self.links.append([node_link, self.p_node_link, bezier])
			self.ind.append(bezier)

			self.is_drawing = 0
			return True

		elif not valid and self.is_drawing:
			self.clear_canvas()
			self.is_drawing = 0

	def node_down(self, obj, touch):
		valid, node, node_link = self._check_nl_collision(touch=touch)
		if valid:
			node._bind(_self=node,
					   nav=node_link._type)
			
			_pos = self.get_pos(node_link, node_link.pos)
			node_link.c_pos = _pos
			
			self.p_node_link = node_link
			self.ori = (_pos[0] + 5, _pos[1] + 5)

			self.is_drawing = 1
			return True

	def get_pos(self, obj, pos):
		_pos = self.to_widget(*obj.to_window(*pos))
		return _pos

	def is_validate(self, obj, touch):
		if self.collide_point(*touch.pos):
			self.children[0].do_translation = True
		else:
			self.children[0].do_translation = False
		return True

	@classmethod
	def _add_node(cls, obj, touch, _self):
		if _self.collide_point(*touch.pos):
			if cls._state == 1:
				pos = _self.children[0].to_local(*touch.pos)
				node = cls._node(spos=pos)

				_self.children[0].add_widget(node)
				cls._state = 0
				cls._node = None
		return True

	def draw(self, ori=None, end=None, clear=True):
		if clear:
			self.clear_canvas()

		with self.canvas:
			bezier = Bezier(points=(ori[0], ori[1],
									(end[0] + ori[0]) / 2 + 20, ori[1],
									(end[0] + ori[0]) / 2 - 20, end[1],
									end[0], end[1]),
							segments=800)
			return bezier

	def clear_canvas(self):
		if len(self.canvas.children) > 1:
			for ins in self.canvas.children:
				if type(ins) == Bezier and ins not in self.ind:
					self.canvas.remove(ins)

	def draw_link(self, obj, touch):
		if self.is_drawing:
			self.draw(self.ori, touch.pos)

	def update_canvas(self, touch, pos):
		if self.collide_point(*touch.pos) and len(self.children[0].children) >= 2 and not self.is_drawing:
			for node in self.children[0].children:
				for node_link in node.children[0].children:
					if type(node_link) == NodeLink:
						for info in self.links:
							if node_link in info and node_link.target in info:
								for bezier in self.canvas.children:
									if bezier in info:
										_pos = self.get_pos(node_link, node_link.pos)

										if _pos != node_link.c_pos and node_link.t_pos != None:
											nl_pos = (node_link.t_pos[0] + 5, node_link.t_pos[1] + 5)
											tl_pos = (_pos[0] + 5, _pos[1] + 5)

											bezier.points = (nl_pos[0], nl_pos[1],
															(tl_pos[0] + nl_pos[0]) / 2 + 20, nl_pos[1],
															(tl_pos[0] + nl_pos[0]) / 2 - 20, tl_pos[1],
															tl_pos[0], tl_pos[1])
											self.ind[self.ind.index(bezier)]

											node_link.c_pos = _pos
											node_link.target.t_pos = _pos


class SubContainer(BoxLayout, Widget):
	pass


class Container(BoxLayout, Widget):
	pass


class _app(App):
	def build(self):
		return Builder.load_file('_template.kv')


if __name__ == '__main__':
	_app().run()
