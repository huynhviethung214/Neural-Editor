import kivy
import sys
from kivy.base import runTouchApp
kivy.require('1.10.1')

from kivy.uix.scatterlayout import ScatterLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.graphics import Line, Rectangle, Bezier, RoundedRectangle
from kivy.uix.label import Label
from functools import partial
from kivy.lang import Builder


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

		self.c_pos = None
		self.t_pos = None
		self.target = None

		self.draw_widget()

	def draw_widget(self):
		with self.canvas:
			Rectangle(pos=self.pos,
					  size=self.size)


class CustomValueInput(BoxLayout):
	def __init__(self, _name, _size, **kwargs):
		super(CustomValueInput, self).__init__()
		self.size = _size

		self._input = TextInput(height=self.height,
							   	font_size=13,
							   	padding=(2, 2, 2, 3),
							   	width=90,
							   	size_hint_x=0.1,
							   	multiline=False)
		
		self._label = Label(text=_name,
						   	halign='center',
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
	m_list = []
	m_names = []
	b_node = None
	in_list = {}
	n_layer = 0

	def __init__(self, spos=(0, 0), **kwargs):
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
		self._type = 1
		self._types = ['Input Layer',
					   'Hidden Layer',
					   'Output Layer']

		self.objs = []
		self.properties = {}

		self.add_components()
		self.add_ib()
		self.combine()
		self.add_info(self.name)
		self.add_custom_properties()

	@classmethod
	def set_id(cls, _type=None, _self=None):
		if _type != None:
			num = cls.m_names.count(_type)
			_self.name = _type + ' {0}'.format(num)
			cls.m_names.append(_type)

		else:
			_self.name = 'Layer {0}'.format(cls.n_layer)
			cls.n_layer += 1

	def add_components(self):
		pass

	def add_custom_properties(self):
		pass

	def algorithm(self):
		return Linear(self.properties['n_in'][1],
					  self.properties['n_out'][1])

	def add_list_data(self, _name, _datas):
		_tf_list = DropDown(auto_width=True)
		_layout = BoxLayout(size_hint=(None, None),
							height=self.ci_height,
							width=self.width - 14)
		self.properties.update({_name: _datas[0]})

		for i in range(0, 2):
			btn = Button(text=str(_datas[i]),
						 size_hint=(0.1, None),
						 width=self.width - 14,
						 height=20)

			btn.bind(on_release=partial(self.set_bool,
										name=_name,
										val=_datas[i],
										button=btn,
										tf_list=_tf_list))
			_tf_list.add_widget(btn)

		drop_butt = Button(text=str(_datas[0]),
						   size_hint=(0.1, None),
						   width=self.width - 14,
						   height=self.ci_height)

		drop_butt.bind(on_release=_tf_list.open)
		_tf_list.bind(on_select=lambda instance, x: setattr(drop_butt, 'text', x))

		_layout.add_widget(Label(text=_name,
							     size_hint_x=None,
							     width=55,
							     halign='right',
							     valign='middle',
							     shorten=True,
							     max_lines=1))

		_layout.add_widget(drop_butt)
		self.add_component(_layout)

	def add_drop_down_list(self):
		self.drop_list = DropDown(auto_width=True)

		for i in range(0, 3):
			btn = Button(text=self._types[i],
						 size_hint=(None, None),
						 width=166,
						 height=20)

			btn.bind(on_release=partial(self._choose_type,
										drop_list=self.drop_list,
										_type=i,
										button=btn))
			self.drop_list.add_widget(btn)

		drop_butt = Button(text='Hidden Layer',
						   width=self.width - 14,
						   height=self.ci_height)

		drop_butt.bind(on_release=self.drop_list.open)
		self.drop_list.bind(on_select=lambda instance, x: setattr(drop_butt, 'text', x))
		self.add_component(drop_butt)

	def set_bool(self, ins, name, val, button, tf_list):
		tf_list.select(button.text)
		self.properties[name] = val

	def _choose_type(self, obj, drop_list, button, _type):
		drop_list.select(button.text)
		self._type = _type

	def add_component(self, obj):
		self.objs.append(obj)
		self.widget_height += obj.height

	def add_id(self):
		self.add_component(Label(text=self.name,
								 height=self.c_height))

	def add_ib(self):
		self.add_component(Label(height=1,
								 size_hint=(None, None)))

	def add_val_input(self, _name, _type):
		input_form = CustomValueInput(_name, _size=(self.width, self.ci_height))
		input_form._input.bind(text=partial(self.set_val, _name=_name))

		self.properties.update({_name: [_type, None]})
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
		self._input_node = NodeLink(spos=(-6,
									(self.height - self.c_height) / 2),
									_type=1)
		self.add_widget(self._input_node)

	def add_output_node(self):
		self._output_node = NodeLink(spos=(self.width-6,
							 		 (self.height - self.c_height) / 2),
				 					 _type=0)
		self.add_widget(self._output_node)

	def draw_border(self):
		with self.canvas:
			Line(rounded_rectangle=(self.layout.x, self.layout.y,
									self.layout.width, self.layout.height,
									6))

	def set_val(self, obj, val, name):
		try:
			if val != '':
				if self.properties[name][0] == int:
					self.properties[name][1] = int(val)

				elif self.properties[name][0] == float:
					self.properties[name][1] = float(val)

				elif self.properties[name][0] == str:
					self.properties[name][1] = val

		except Exception:
			obj.text = ''

	@classmethod
	def _is_exist(cls, _list):
		if _list in cls.m_list:
			return True
		return False

	@classmethod
	def _bind(cls, _self=None, state=1, nav=None):
		if state == 1:
			cls.b_node = _self
			cls.b_node.c_nav = nav

		elif state == 2:
			temp_list = []
			_existed = False

			if _self is not None and cls.b_node is not None:
				if _self.name != cls.b_node.name and nav != cls.b_node.c_nav:
					if cls.in_list[cls.b_node.name][nav] == None and cls.in_list[_self.name][cls.b_node.c_nav] == None:
						if cls.b_node.name != _self.name:
							temp_list.append(cls.b_node)
							temp_list.insert(nav, _self)
							_existed = _self._is_exist(temp_list)

							if _existed == False:
								cls.m_list.append(temp_list)

							cls.in_list[cls.b_node.name][nav] = _self.name
							cls.in_list[_self.name][cls.b_node.c_nav] = cls.b_node.name

					else:
						temp_list.append(cls.b_node)
						temp_list.insert(nav, _self)

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
						_existed = _self._is_exist(temp_list)

						if _existed == False:
							cls.m_list.append(temp_list)
					cls.b_node = None
		# print(cls.m_list)

	@classmethod
	def unbind(cls, obj=None, nav=None):
		for layer in cls.m_list:
			if obj.target.parent.parent != layer[nav]:
				cls.m_list.remove(layer)
		# print(cls.m_list)

	@classmethod
	def add_info(cls, _alg):
		cls.in_list.update({_alg: [None, None]})


if __name__ == '__main__':
	runTouchApp(Node())