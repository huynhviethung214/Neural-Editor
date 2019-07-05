import kivy
import sys
from kivy.base import runTouchApp
kivy.require('1.10.1')

from kivy.uix.scatterlayout import ScatterLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.scatter import Scatter
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.graphics import Line, Rectangle, Bezier, RoundedRectangle
from kivy.uix.label import Label
from kivy.clock import Clock
from functools import partial


class NodeLink(Widget):
	b_node = None
	u_node = None
	ctd_state = {}

	def __init__(self, spos, _type, **kwargs):
		super(NodeLink, self).__init__()
		self.size_hint = (None, None)
		self.size = (12, 12)
		self.pos = spos
		self._type = _type

		self.draw_widget()

	def draw_widget(self):
		with self.canvas:
			Rectangle(pos=self.pos,
					  size=self.size)


class CustomValueInput(BoxLayout):
	def __init__(self, _name, _size, **kwargs):
		super(CustomValueInput, self).__init__()
		self.orientation = 'horizontal'
		self.size = _size

		self._input = TextInput(height=self.height,
						   font_size=13,
						   padding=(2, 2, 2, 3),
						   width=90,
						   size_hint_x=0.1,
						   multiline=False)
		
		self._label = Label(text=_name + ':',
					   halign='right',
					   valign='middle',
					   width=50,
					   max_lines=1,
					   shorten=True)
		self._label.text_size = (50, 35)
		self._label.size_hint_x = 0.05

		self.add_widget(self._label)
		self.add_widget(self._input)


class Node(ScatterLayout):
	c_height = 35
	c_padding = 5
	c_spacing = 2
	ci_height = 20
	# 0 = BEGIN, 1 = END, 2 = UNBIND
	# m_list = [0, 1]
	m_list = []
	b_node = None
	in_list = {}
	n_layer = 1

	def __init__(self, spos=(0, 0), name=None, **kwargs):
		super(Node, self).__init__()
		self.layout = AnchorLayout(anchor_x='center',
								   anchor_y='center')
		self.sub_layout = BoxLayout()
		self.sub_layout.orientation = 'vertical'

		self.do_scale = False
		self.do_rotation = False
		self.size_hint = (None, None)
		self.width = 180

		self.pos = spos
		self.widget_height = 0
		self.c_nav = None
		self.node_pos = []

		if name == None:
			self.name = self.set_name()
		else:
			self.name = name

		self.objs = []
		self.layer_properties = {}

		self.add_id(self.name)
		self.add_val_input('Float', float)
		self.add_val_input('String', str)
		self.add_val_input('Int', int)
		self.add_ib()
		self.combine()

		self.add_info(self.name)

	def add_component(self, obj):
		self.objs.append(obj)
		self.widget_height += obj.height

	def add_id(self, _id):
		self.add_component(Label(text=_id,
								 height=self.c_height))

	def add_ib(self):
		self.add_component(Label(height=1,
								 size_hint=(None, None)))

	def add_button(self, _name):
		self.add_component(Button(text=_name,
								  height=self.c_height))

	def add_val_input(self, _name, _type):
		input_form = CustomValueInput(_name, _size=(self.width, self.ci_height))
		input_form._input.bind(text=partial(self.set_val, _name=_name))

		self.layer_properties.update({_name: [_type, None]})
		self.add_component(input_form)

	def combine(self):
		self.sub_layout.padding = (7, self.c_padding, 7, self.c_padding)
		self.sub_layout.spacing = self.c_spacing

		for obj in self.objs:
			self.sub_layout.add_widget(obj)

		self.widget_height += self.c_spacing + self.c_padding * 2
		self.height = self.widget_height
		self.layout.size = self.size

		self.layout.add_widget(self.sub_layout)
		self.add_widget(self.layout)
		self.draw_border()
		self.add_output_node()
		self.add_input_node()

	def add_input_node(self):
		self._input_node = NodeLink(spos=(-6, (self.height - self.c_height) / 2),
									_type=1)
		self._input_node.bind(on_touch_up=self._node_up)
		self._input_node.bind(on_touch_down=self._node_down)

		_parent_cord = self.to_parent(*self._input_node.pos)
		self.node_pos.append(_parent_cord)
		self.add_widget(self._input_node)

	def add_output_node(self):
		self._output_node = NodeLink(spos=(self.width-6,
							 		 (self.height - self.c_height) / 2),
				 					 _type=0)
		self._output_node.bind(on_touch_up=self._node_up)
		self._output_node.bind(on_touch_down=self._node_down)

		_parent_cord = self.to_parent(*self._output_node.pos)
		self.node_pos.append(_parent_cord)
		self.add_widget(self._output_node)

	def draw_border(self):
		with self.canvas:
			Line(points=(self.layout.x, self.layout.y,
						 self.layout.x, self.layout.y + self.layout.height,
						 self.layout.x+ self.layout.width, self.layout.y + self.layout.height,
						 self.layout.x+ self.layout.width, self.layout.y,
						 self.layout.x, self.layout.y),
				 width=2)

	def alg(self):
		return 'Alg {0}'.format(self.name)

	def set_val(self, obj, val, _name):
		try:
			if val != '':
				if self.layer_properties[_name][0] == int:
					self.layer_properties[_name][1] = int(val)

				elif self.layer_properties[_name][0] == float:
					self.layer_properties[_name][1] = float(int(val))
		
		except Exception:
			obj.text = ''

	def _node_up(self, obj, touch):
		if obj.collide_point(*touch.pos):
			self._bind(_self=self,
					   state=2,
					   nav=obj._type)
			return True

	def _node_down(self, obj, touch):
		if obj.collide_point(*touch.pos):
			self._bind(_self=self,
					   nav=obj._type)
			return True

	#TODO: CREATE A SORTING ALGORITHM & A CONCATING ALGORITHM
	@classmethod
	def _bind(cls, _self=None, state=1, nav=None):
		if state == 1:
			cls.b_node = _self
			cls.b_node.c_nav = nav

		elif state == 2:
			temp_list = []
			
			if _self is not None and cls.b_node is not None:
				if _self.name != cls.b_node.name and nav != cls.b_node.c_nav:
					if cls.in_list[cls.b_node.name][nav] == None and cls.in_list[_self.name][cls.b_node.c_nav] == None:
						if cls.b_node.name != _self.name:
							temp_list.append(cls.b_node.name)
							temp_list.insert(nav, _self.name)
							cls.m_list.append(temp_list)

							cls.in_list[cls.b_node.name][nav] = _self.name
							cls.in_list[_self.name][cls.b_node.c_nav] = cls.b_node.name
					else:
						temp_list.append(cls.b_node.name)
						temp_list.insert(nav, _self.name)

						# Cancel the previous connection
						# print(cls.in_list[cls.b_node.alg()][cls.b_node.c_nav])
						# print(cls.in_list[_self.alg()][nav])

						if cls.in_list[cls.b_node.name][nav] != None:
							for layer in cls.m_list:
								if cls.in_list[cls.b_node.name][nav] in layer and cls.b_node.name in layer:
									cls.m_list.remove(layer)
							cls.in_list[cls.in_list[cls.b_node.name][nav]][cls.b_node.c_nav] = None

						if cls.in_list[_self.name][cls.b_node.c_nav] != None:
							for layer in cls.m_list:
								if cls.in_list[_self.name][cls.b_node.c_nav] in layer and _self.name in layer:
									cls.m_list.remove(layer)
							cls.in_list[cls.in_list[_self.name][cls.b_node.c_nav]][nav] = None
						
						cls.in_list[cls.b_node.name][nav] = _self.name
						cls.in_list[_self.name][cls.b_node.c_nav] = cls.b_node.name	
						cls.m_list.append(temp_list)
					cls.b_node = None

					# print(cls.m_list) 
					# print(cls.in_list)

	@classmethod
	def add_info(cls, _alg):
		cls.in_list.update({_alg: [None, None]})

	@classmethod
	def set_name(cls):
		n = 'Layer {0}'.format(cls.n_layer)
		cls.n_layer += 1
		return n


if __name__ == '__main__':
	runTouchApp(Node())