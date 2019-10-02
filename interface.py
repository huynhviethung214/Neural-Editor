import kivy
import torch
from kivy.app import runTouchApp
from torchsummary import summary
kivy.require('1.10.1')

from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.progressbar import ProgressBar
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.stencilview import StencilView
from kivy.uix.treeview import TreeViewLabel, TreeView
from kivy.graphics import Bezier
from kivy.lang import Builder
from kivy.properties import StringProperty, ListProperty
from kivy.app import App
from functools import partial
from node import Node, NodeLink
from utils import Sorter, Net
from torch.nn import Sequential, Module, CrossEntropyLoss, ParameterList
from nn_components import Linear, XConv2d, Flatten
from processors import _ImageProcessor
from math import floor


device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')


class _ProgressBar(ProgressBar):
	def _train(self, model=None, dataset=None, epochs=10, is_save=True, w_name='weights'):
		criterion = CrossEntropyLoss()
		optimizer = torch.optim.Adam(ParameterList(model.parameters()),
									lr=0.001)

		for epoch in range(1, epochs):
			for i, (X, y) in enumerate(dataset[0]):
				output = model(X)
				loss = criterion(output, y).to(device)

				model.zero_grad()
				loss.backward()
				optimizer.step()
				self._update(epoch / epochs)
		self._evaluate(dataset)

		if is_save:
			torch.save(model.state_dict(),
					   '{0}.prmt'.format(w_name))

	def _evaluate(self, dataset=None, epochs=20):
		self.value = 0

		with torch.no_grad():
			score = 0

			for epoch in range(epochs):
				# self._update(epochs)
				
				for (X, y) in dataset[1]:
					output = model(X)
					pred = torch.argmax(output)
					target = y.tolist()[0]
					pred = pred.item()

				if target == pred:
					score += 1

	def _update(self, val):
		self.value = val


class TrainButton(Button):
	net = Net

	def __init__(self, **kwargs):
		super(TrainButton, self).__init__()
		self.text = 'Train'
		self.bind(on_touch_down=self.train)
		self.sorter = Sorter()

	def train(self, obj, touch):
		if self.collide_point(*touch.pos):
			self.sorter.setup(Node.m_list)
			# self.sorter.sort(Node.m_list)
			# print(Node.m_list)
			# print(Sorter.temp_model)
			model = self.sorter.sort(Node.m_list)
			dataset = DatasetForm.processor._dataset()
			# print(model, (1, 300, 300))
			self.parent.children[0]._train(model, dataset, 100)


class ComponentPanel(TreeView, Widget):
	def __init__(self, **kwargs):
		super(ComponentPanel, self).__init__()
		self.root_options = {'text': 'Component Panel'}
		self.add_node(Linear(interface=Interface))
		self.add_node(XConv2d(interface=Interface))
		self.add_node(Flatten(interface=Interface))


class DatasetForm(BoxLayout, Widget):
	processor = _ImageProcessor()


class Form(BoxLayout, Widget):
	name = StringProperty()
	_type = None

	def set_val(self, val, tag, obj):
		try:
			if val != '':
				if self._type == int:
					self.parent.processor.properties[self.name] = int(val)

				elif self._type == float:
					self.parent.processor.properties[self.name] = float(val)

				elif self._type == bool:
					self.parent.processor.properties[self.name] = bool(val)

				elif self._type == str:
					self.parent.processor.properties[self.name] = val

		except Exception:
			obj.text = ''


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

	def draw(self, ori=None, end=None):
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


class Container(BoxLayout, Widget):
	pass


class _app(App):
	def build(self):
		return Builder.load_file('interface_template.kv')


if __name__ == '__main__':
	_app().run()
