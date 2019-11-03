import kivy
import torch
from inspect import signature
from kivy.app import runTouchApp
from torchsummary import summary
from math import floor
from threading import Thread
from bs4 import BeautifulSoup
from urllib.request import urlopen
from time import sleep
from queue import Queue
kivy.require('1.10.1')

from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.progressbar import ProgressBar
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.stencilview import StencilView
from kivy.uix.treeview import TreeViewLabel, TreeView
from kivy.uix.dropdown import DropDown
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.graphics import Bezier
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.scrollview import ScrollView
from kivy.app import App
from functools import partial
from node import Node, NodeLink
from utils import Sorter, Net
from torch.nn import Sequential, Module, CrossEntropyLoss, ParameterList
from nn_components import Linear, XConv2d, Flatten
from processors import _ImageProcessor


device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')


# class ThreadManager():
# 	def __init__(self):
# 		self.threads = {}

# 	def register_thread(self, _id, func, **kwargs):
# 		thread = Thread(target=func,
# 						kwargs=kwargs,
# 						daemon=True)
# 		self.threads.update({_id: thread})

# 	def start_thread(self, _id):
# 		self.threads[_id].start()

# 	def kill_thread(self, _id):
# 		self.threads[_id].join()


class _ProgressBar(ProgressBar):
	def kill_process(self):
		self._break = True
		self._train_thread.join()
		self.parent.children[0].text = '[{0}]:[0%/100%]'.format(_type)

	def train(self, model=None, dataset=None, epochs=10, is_save=True, w_name='weights'):
		self._train_thread = Thread(target=self._train,
									args=(model, dataset, epochs, is_save, w_name,),
									daemon=True)
		self._break = False
		self.std_val = (1 / epochs) * 100

		self.parent.children[0].text = '[Train]:[0%/{0}%]'.format(epochs)
		self._train_thread.start()

	def _train(self, model=None, dataset=None, epochs=10, is_save=True, w_name='weights'):
		# criterion = CrossEntropyLoss()
		criterion = CriterionForm._constructed_func
		optimizer = torch.optim.Adam(ParameterList(model.parameters()),
									lr=0.001)
		self.max = 100

		for epoch in range(1, epochs):
			for i, (X, y) in enumerate(dataset[0]):
				if self._break:
					break
				
				output = model(X)
				loss = criterion(output, y).to(device)

				model.zero_grad()
				loss.backward()
				optimizer.step()
				# self.queue.put(epoch / epochs)
				self._update((epoch / epochs) * 100, 'Train')
				# print(epoch)

				# if i % 100 == 0:
				# 	print('[{0}: {1}]-->[Prediction:{2} | Expected Prediction: {3}]'.format(epoch, loss, torch.argmax(output), y))
		self._update(100, 'Train')
		torch.cuda.empty_cache()

		self._evaluate(model, dataset)

		if is_save:
			torch.save(model.state_dict(),
					'{0}.prmt'.format(w_name))
		torch.cuda.empty_cache()

	def _evaluate(self, model=None, dataset=None, epochs=20):
		self.value = 0

		with torch.no_grad():
			score = 0

			for epoch in range(epochs):
				for (X, y) in dataset[1]:
					output = model(X)
					pred = torch.argmax(output)
					target = y.tolist()[0]
					pred = pred.item()
					self._update((epoch / epochs) * 100, 'Eval')

				if target == pred:
					score += 1

			self._update(100, 'Eval')
		# print('Accuracy: {0}'.format((score / len(dataset[1])) * 100))

	# def free_momery(self):
	# 	torch.cuda.empty_cache()

	def _update(self, val, _type):
		# self.value += int(floor(100 / epochs))
		self.value = val
		self.parent.children[0].text = '[{0}]:[{1}%/100%]'.format(_type, int(floor(val)))


class IndicatorLabel(Label):
	def __init__(self, **kwargs):
		super(IndicatorLabel, self).__init__()
		# self.bind(size=self.update)

	def update(self, obj, val):
		self.font_size = (self.parent.width * 0.3,
						self.parent.height * 0.3)


class KillProcessButton(Button):
	def __init__(self, **kwargs):
		super(KillProcessButton, self).__init__()
		self.bind(on_touch_down=self._kill_process)

	def _kill_process(self, obj, touch):
		if self.collide_point(*touch.pos):
			try:
				self.parent.children[1].kill_process()
			except Exception:
				pass


class TrainButton(Button):
	net = Net

	def __init__(self, **kwargs):
		super(TrainButton, self).__init__()
		self.bind(on_touch_down=self.train)
		self.sorter = Sorter()

	#TODO: DO THE DATA PROCESSING ON A SEPARATE THREAD
	def train(self, obj, touch):
		if self.collide_point(*touch.pos):
			# print(self.parent.children)
			try:
				self.sorter.setup(Node.m_list)
				# self.sorter.sort(Node.m_list)
				# print(Node.m_list)
				# print(Sorter.temp_model)
				model = self.sorter.sort(Node.m_list)
				dataset = DatasetForm.processor._dataset()
				# print(model, (1, 300, 300))
				# self.parent.children[0]._train(model, dataset, 100)
				self.parent.children[1].train(model, dataset, 100)

			except Exception as e:
				print(e)


class ComponentPanel(TreeView, Widget):
	def __init__(self, **kwargs):
		super(ComponentPanel, self).__init__()
		self.root_options = {'text': 'Component Panel'}
		self.add_node(Linear(interface=Interface))
		self.add_node(XConv2d(interface=Interface))
		# self.add_node(ImageDataProcessor(interface=Interface))
		self.add_node(Flatten(interface=Interface))


class DatasetForm(BoxLayout, Widget):
	processor = _ImageProcessor()


#TODO: TRY TO COMPLETE OTF AND CTRF
class OptimizerForm(BoxLayout, Widget):
	pass


#TODO: MANUALLY ADDING CRITERION USING PYTORCH.ORG TO GET THE VALUE TYPE
class CriterionForm(BoxLayout, Widget):
	# _constructed_func = None
	# sub_layout = ObjectProperty(None)

	def __init__(self, **kwargs):
		super(CriterionForm, self).__init__()
		self.sub_layout = BoxLayout(orientation='vertical',
									size_hint=(1, None),
									spacing=30)
		self.sub_layout.bind(minimum_height=self.sub_layout.setter('height'))
		self.orientation = 'vertical'
		# self._criterions = {}
		self.properties = {}
		self.add_func_list()
		self.add_scroll_view()
		# self.generator(self.criterion[0])
		self.add_widget(self.scroll_view)

	def add_scroll_view(self):
		self.scroll_view = ScrollView(size_hint_x=1,
									height=self.height)
		self.scroll_view.add_widget(self.sub_layout)

	def add_func_list(self):
		funcs = self.get_func()
		crit_chooser = Spinner(text=funcs[0],
								values=tuple(funcs),
								size_hint=(1, None),
								height=25,
								sync_height=True)
		crit_chooser.bind(text=self.generator)

		self.generator(None, funcs[0])
		self.add_widget(crit_chooser)

	def generator(self, obj, optim):
		self.sub_layout.clear_widgets()
		for key in self.properties[optim].keys():
			self.add_subform(key,
							self.properties[optim][key][0],
							self.properties[optim][key][1])
		# self.set_func_args_form(optim)
		# self.construct_function()
		# self.crit_chooser.text = optim
		# for prop in self._criterions[optim]._properties:
		# 	# print(optim._properties[prop][0])
		# 	self.add_subform(prop,
		# 					self._criterions[optim]._properties[prop][0],
		# 					self._criterions[optim]._properties[prop][1])
		# pass

	# @staticmethod
	def parse_data(self, fname):
		html = 'https://pytorch.org/docs/stable/nn.html#l1loss'
		soup = BeautifulSoup(urlopen(html), "lxml")
		div = soup.findAll(attrs={'id': fname})
		vals = BeautifulSoup(str(div), 'lxml')
		vals = vals.findAll(attrs={'class': 'sig-param'})

		convert_list = {'string': str,
						'int': int,
						'bool': bool,
						'float': float,
						'Sequence': list,
						'Tensor': 'Tensor'}
		l = []

		for val in vals:
			info = val.text
			l.append([info.split('=')[0], [None, info.split('=')[1]]])

		field = BeautifulSoup(str(div), 'lxml')
		field = field.findAll(attrs={'class': 'field-odd'})

		i = 0
		for _field in field:
			_type = _field.findAll('em')
			for t in _type:
				if t.text != ', ' and t.text != 'optional':
					l[i][1][0] = convert_list[t.text]
					i += 1
		return dict(l)

	def get_func(self):
		fnames = []
		for func in dir(torch.nn):
			if 'Loss' in func:
				try:
					prop = self.parse_data(func.lower())
					self.properties.update({func: prop})
					if len(prop.keys()) >= 1:
						fnames.append(func)
						self.properties.pop(prop)
				except Exception:
					pass
		return fnames

	# def set_tf(self, obj, val, _id):
	# 	self.properties[_id] = bool(val)
		# tf_butt.text = str(val)

	# def construct_function(self):
	# 	_kwargs = {}
	# 	for _id in self.properties.keys():
	# 		# if self.properties[_id] != None:
	# 		# 	_kwargs.update({_id:self.properties[_id]})
	# 		# elif self.properties[_id] == None:
	# 		# 	_kwargs.update({_id:None})
	# 		# print(_id, ' ', self.properties[_id])
	# 		_kwargs.update({_id:self.properties[_id]})
	# 	CriterionForm._constructed_func = self.func(**_kwargs)

	# def set_val(self, obj, val, _type, _id):
	# 	try:
	# 		if val != '':
	# 			if _type == int:
	# 				self.properties[_id] = int(val)

	# 			elif _type == float:
	# 				self.properties[_id] = float(val)

	# 			elif _type == str:
	# 				self.properties[_id] = val

	# 	except Exception:
	# 		obj.text = ''

	def tf_drop_list(self, _id, d_val):
		tf_butt = Spinner(text=str(d_val),
						values=('True', 'False'),
						size_hint=(0.6, None),
						height=26,
						sync_height=True)
		# self.properties[_id] = d_val

		# tf_butt.bind(text=lambda obj, text: setattr(self, 'properties[{0}]'.format(_id),
		# 											bool(text)))

		return tf_butt

	def boolean_form(self, _id, d_val):
		bool_subform = BoxLayout(height=30)
		bool_subform.add_widget(Label(text=_id,
									height=26,
									size_hint=(0.3, None)))
		bool_subform.add_widget(self.tf_drop_list(_id, d_val))
		return bool_subform

	def _subform(self, _id, _type, d_val):
		subform = BoxLayout(height=30)
		subform.add_widget(Label(text=_id,
								size_hint=(0.3, None),
								height=26))

		_input = TextInput(height=26,
							font_size=15,
							padding=(2, 2, 2, 3),
							size_hint=(0.6, None),
							multiline=False,
							text=str(d_val))

		# self.properties[_id] = d_val
		# _input.bind(text=partial(self.set_val,
		# 						_type=_type,
		# 						_id=_id))
		subform.add_widget(_input)
		return subform

	def add_subform(self, _id, _type, d_val):
		if _type == bool:
			self.sub_layout.add_widget(self.boolean_form(_id, d_val))
		else:
			self.sub_layout.add_widget(self._subform(_id, _type, d_val))

	# PARSE DEFAULT VALUE AND ARGUMENT TYPE ERROR OCCUR BECAUSE 
	# OF ADAPTIVELOGSOFTMAXWITHLOSS FUNCTION
	# def add_form(self, params):
	# 	val = None
	# 	_id = None
	# 	_type = None

	# 	for pval in params.parameters.values():
	# 		try:
	# 			val = str(pval).split('=')[1]
	# 			_id = str(pval).split('=')[0]

	# 			if 'False' == val or 'True' == val:
	# 				_type = bool
	# 				val = bool(val)

	# 			elif '\'' in val:
	# 				_type = str
	# 				val = val.split('\'')[1]

	# 			elif '.' in val:
	# 				_type = float
	# 				val = float(val)

	# 			else:
	# 				_type = int
	# 				val = int(val)

	# 		except Exception:
	# 			val = None
	# 			_type = int

	# 		self.add_subform(_id, _type, val)
			# print(_id, val, _type)

	# def set_func_args_form(self, func_name):
	# 	for func in self.get_func():
	# 		if func == func_name:
	# 			module = __import__('torch.nn', fromlist=[func_name])
	# 			self.func = getattr(module, func_name)
	# 			params = signature(self.func)
	# 			self.add_form(params)

	# 			for param in params.parameters:
	# 				# print(param)
	# 				# print(params.parameters[param])
	# 				self.add_subform(_id=param,
	# 								_type=self.get_type(params))
	# 				self.properties.update({param:None})


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

							# node_link.target.t_pos = None
							# node_link.target.target = None

							# node_link.target = None
							# node_link.t_pos = None

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


# class _app(App):
# 	def build(self):
# 		return Builder.load_file('interface_template.kv')


# if __name__ == '__main__':
# 	_app().run()
