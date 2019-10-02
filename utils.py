import torch
from torch.nn import Module, Sequential, ModuleList

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

class Sorter(object):
	temp_model = []
	train_set = None
	test_set = None
	indicator = None

	@staticmethod
	def setup(layers):
		for layer in layers:
			for node in layer:
				if node._type == 0:
					Sorter.temp_model.insert(0, layer[0])
					Sorter.indicator = layer[1]

				elif node._type == 2:
					Sorter.temp_model.insert(1, layer[1])

	@staticmethod
	def _model(layers):
		for layer in layers:
			if layer != None:
				Net.model.append(layer)
		return Net().to(device)

	def sort(self, layers):
		c_ind = Sorter.indicator
		ci = 1

		# SORTING ALGORITHM
		for layer in layers[1:]:
			if layer[0] == c_ind:
				Sorter.temp_model.insert(ci, layer[0])
				ci += 1
				c_ind = layer[1]

		#EXTRACTING LAYER OUT OF AN ARRAY OF LAYERS
		model = []
		for block in Sorter.temp_model:
			model.append(block.algorithm())

		return self._model(model)


class Net(Module):
	model = []

	def __init__(self, **kwargs):
		super(Net, self).__init__()
		self.blocks = ModuleList()

		for layer in Net.model:
			self.blocks.append(layer)

	def forward(self, x):
		out = x
		for block in self.blocks:
			out = block(out)
		return out


class _Flatten(Module):
	def forward(self, x):
		return x.view(x.size()[0], -1)
