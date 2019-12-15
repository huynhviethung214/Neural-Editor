from nn_modules.node import Node
from torch.nn import ReLU, BatchNorm2d, Conv2d, MaxPool2d, Linear, Sequential


class LinearNode(Node):
	def add_components(self):
		self.set_id(_type='Linear', _self=self)
		self.add_id()
		self.add_drop_down_list()
		self.add_val_input('n_in', int)
		self.add_val_input('n_out', int)
		self.add_list_data('bias', [True, False])

	def algorithm(self):
		return Linear(self.properties['n_in'][1],
					  self.properties['n_out'][1],
					  self.properties['bias'])


class _XConv2d(Node):
	def add_components(self):
		self.set_id(_type='XConv2d', _self=self)
		self.add_id()
		self.add_drop_down_list()
		self.add_val_input('n_in', int)
		self.add_val_input('n_out', int)
		self.add_val_input('f_size', int)
		self.add_val_input('stride', int)
		self.add_val_input('padding', int)
		self.add_val_input('b_norm', int)
		self.add_val_input('mpk_size', int)
		self.add_val_input('mp_stride', int)

	def algorithm(self):
		n_in = self.properties['n_in'][1]
		n_out = self.properties['n_out'][1]
		f_size = self.properties['f_size'][1]
		stride = self.properties['stride'][1]
		padding = self.properties['padding'][1]
		b_norm = self.properties['b_norm'][1]
		mpk_size = self.properties['mpk_size'][1]
		mp_stride = self.properties['mp_stride'][1]

		return Sequential(Conv2d(in_channels=n_in, out_channels=n_out, kernel_size=f_size, stride=stride, padding=padding),
						BatchNorm2d(b_norm),
						ReLU(),
						MaxPool2d(kernel_size=mpk_size, stride=mp_stride))
