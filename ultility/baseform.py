from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.spinner import Spinner
from ultility.base_properties import BaseListForm, BaseInputForm
from functools import partial
import torch


# class BaseForm(BoxLayout, Widget):
# 	def __init__(self, **kwargs):
# 		super(BaseForm, self).__init__()
# 		self.src = None
# 		self.form_type = None
# 		self.c_func = None

# 		self.properties = {}
# 		self.fnames = []
# 		self.convert_list = {'string': str,
# 							'int': int,
# 							'bool': bool,
# 							'float': float,
# 							'Sequence': list,
# 							'Tensor': 'Tensor', # FIND SOME SOLUTION TO DEAL WITH THIS
# 							'Tuple': tuple, # SCRAPPING "d_val" FROM THIS
# 							'iterable': list} # AND THIS

# 	def init(self):
# 		self.sub_layout = BoxLayout(orientation='vertical',
# 									size_hint=(1, None),
# 									padding=0,
# 									spacing=2)
# 		self.sub_layout.bind(minimum_height=self.sub_layout.setter('height'))

# 		self.get_fnames()
# 		self.add_func_list()
# 		self.add_scroll_view()
# 		self.add_widget(self.scroll_view)

# 	def add_scroll_view(self):
# 		self.scroll_view = ScrollView(size_hint=(1, 1))
# 		self.scroll_view.add_widget(self.sub_layout)

# 	def add_func_list(self):
# 		crit_chooser = Spinner(text=self.fnames[0],
# 								values=tuple(self.fnames),
# 								size_hint=(1, None),
# 								height=20,
# 								sync_height=True)
# 		crit_chooser.bind(text=self.generator)

# 		self.generator(None, self.fnames[0])
# 		self.add_widget(crit_chooser)

# 	def generator(self, obj, func):
# 		self.sub_layout.clear_widgets()
# 		self.c_func = func

# 		for key in self.properties[func].keys():
# 			self.add_subform(key,
# 							self.properties[func][key][0],
# 							self.properties[func][key][1])

# 	def parse_data(self, fname):
# 		soup = BeautifulSoup(urlopen(self.src), "lxml")
# 		sects = soup.findAll(attrs={'id': fname, 'class': 'section'})

# 		sect1 = BeautifulSoup(str(sects[0]), 'lxml')
# 		sect1 = sect1.findAll(attrs={'class': 'class'})

# 		sect2 = BeautifulSoup(str(sects[0]), 'lxml')
# 		sect2 = sect2.findAll('ul')

# 		lis = BeautifulSoup(str(sect2[0]), 'lxml')
# 		lis = lis.findAll('li')

# 		_vars = BeautifulSoup(str(sect1[0]), 'lxml')
# 		_vars = _vars.findAll(attrs={'class': 'sig-param'})

# 		nval = 0
# 		ntype = 0
# 		x = 0

# 		_vars_list = []
# 		bools = []
# 		types = []

# 		for li in lis:
# 			_li = BeautifulSoup(str(li), 'lxml')
# 			pres = _li.findAll(attrs={'class': 'pre'})
# 			ems = _li.findAll('em')

# 			for em in ems:
# 				if em.text != ', ' and em.text != 'optional':
# 					types.append(em.text)
# 					ntype += 1

# 			try:
# 				if pres[-1].text == 'False' or pres[-1].text == 'True':
# 					bools.append(pres[-1].text)

# 			except Exception:
# 				pass

# 		for i, var in enumerate(_vars):
# 			info = var.text.split('=')
# 			d_val = info[1]

# 			if "'" in info[1]:
# 				d_val = info[1].split("'")[1]

# 			if info[1] == 'None':
# 				d_val = bools[x]
# 				x += 1

# 			_vars_list.append([info[0], [self.convert_list[types[i]], d_val]])
# 			nval += 1

# 		if ntype == nval:
# 			return dict(_vars_list)

# 	def process_prop(self):
# 		pcd_prop = {}
# 		# TODO: WE HAVE TO DEAL WITH TENSOR DATA TYPE
# 		for key in self.properties[self.c_func].keys():
# 			if self.properties[self.c_func][key][1] != 'None':
# 				pcd_prop.update({key: self.properties[self.c_func][key][0](self.properties[self.c_func][key][1])})
# 		return pcd_prop

# 	def get_func(self):
# 		module = __import__('torch.nn', fromlist=[self.c_func])
# 		func = getattr(module, self.c_func)
# 		return func(**self.process_prop())

# 	def init_properties(self, func):
# 		try:
# 			prop = self.parse_data(func.lower())

# 			if prop != None:
# 				self.fnames.append(func)
# 				self.properties.update({func: prop})

# 		except Exception as e:
# 			pass

# 	def get_fnames(self):
# 		for func in dir(torch.nn):
# 			if self.form_type == 0: # 0 = LOSS FUNCTION
# 				if 'Loss' in func:
# 					self.init_properties(func)

# 			elif self.form_type == 1: # 1 = OPTIMIZER FUNCTION
# 				if func[0].isupper():
# 					self.init_properties(func)

# 	def tf_drop_list(self, _id, d_val):
# 		tf_butt = Spinner(text=str(d_val),
# 						values=('True', 'False'),
# 						size_hint=(0.6, None),
# 						height=26,
# 						sync_height=True)

# 		tf_butt.bind(text=lambda obj, text: setattr(self, 'properties[{0}][{1}][1]'.format(self.c_func, _id),
# 													bool(text)))

# 		return tf_butt

# 	def boolean_form(self, _id, d_val):
# 		bool_subform = BoxLayout(height=30, size_hint_y=None)
# 		bool_subform.add_widget(Label(text=_id,
# 									height=26,
# 									size_hint=(0.3, None)))
# 		bool_subform.add_widget(self.tf_drop_list(_id, d_val))
# 		return bool_subform

# 	def _subform(self, _id, _type, d_val):
# 		subform = BoxLayout(height=30, size_hint_y=None)
# 		subform.add_widget(Label(text=_id,
# 								size_hint=(0.3, None),
# 								height=26))

# 		_input = TextInput(height=26,
# 							font_size=15,
# 							padding=(5, 2, 2, 3),
# 							size_hint=(0.6, None),
# 							multiline=False,
# 							text=str(d_val),
# 							border=(0, 0, 0, 0))

# 		_input.bind(text=lambda obj, text: setattr(self, 'properties[{0}][{1}][1]'.format(self.c_func, _id),
# 												_type(text)))

# 		subform.add_widget(_input)
# 		return subform

# 	def add_subform(self, _id, _type, d_val):
# 		if _type == bool:
# 			self.sub_layout.add_widget(self.boolean_form(_id, d_val))
# 		else:
# 			self.sub_layout.add_widget(self._subform(_id, _type, d_val))


class BaseForm(BoxLayout, Widget):
	def __init__(self, **kwargs):
		super(BaseForm, self).__init__()
		self.properties = {} # FORMAT: {NAME: [DTYPE, DVAL, []]}

		self.add_properties()
		self.build_form()

	def add_properties(self):
		pass

	def build_form(self):
		for prop in self.properties.keys():
			if self.properties[prop][0] == (int or float or str):
				self.add_inputform(prop, self.properties[prop])
			
			elif self.properties[prop][0] == (list or dict or 'Tensor'):
				pass

			elif self.properties[prop][0] == bool:
				self.add_listform(prop, self.properties[prop])

	# def register_property(self, info):
	# 	self.parent.properties.update({info[0]: [info[1], info[2]]})

	def add_inputform(self, name, dval, dtype):
		input_form = BaseInputForm(dtype=dtype,
								dval=dval,
								name=name)
		input_form.children[0].bind(text=partial(self.bind_prop,
												name=name,
												dtype=dtype))
		# self.register_property([dname, dtype, dtype(dval)])
		self.add_widget(input_form)

	def add_listform(self, name, dval, dtype, values):
		list_form = BaseListForm(dtype=dtype,
								dval=dval,
								name=name,
								values=values)
		list_form.children[0].bind(text=partial(self.bind_prop,
												name=name,
												dtype=dtype))
		# self.register_property([dname, dtype, dtype(dval)])
		self.add_widget(list_form)

	def bind_prop(self, obj, value, name, dtype):
		# self.parent.properties[name][1] = self.parent.properties[name][0](value)
		pass

# from kivy.app import runTouchApp

# class Tester(BaseForm):
# 	def add_properties(self):
# 		self.add_inputform(name='epoch', dval=10, dtype=int)
# 		self.add_listform(name='bool', dval=1, dtype=bool, values=['1', '0'])
# 		self.add_inputform(name='float', dval=10.0, dtype=float)

# runTouchApp(Tester())