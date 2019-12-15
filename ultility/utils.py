import torch
from torch.nn import Module, Sequential, ModuleList

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')


# FIX THE SORTING ALGORITHM
class Sorter(object):
	temp_model = []
	train_set = None
	test_set = None
	indicator = None

	@staticmethod
	def setup(layers):
		# print(layers)
		# print('====')

		for layer in layers:
			for node in layer:
				if node.type == 0:
					Sorter.temp_model.insert(0, layer[0])
					# Sorter.temp_model.insert(1, layer[1])
					Sorter.indicator = layer[1]
					# layers.remove(layer)

				elif node.type == 2:
					Sorter.temp_model.insert(1, layer[1])
					# Sorter.temp_model.insert(len(Sorter.temp_model)-1, layer[0])
					# layers.remove(layer)

				# elif node._type == 3:
				# 	Sorter.train_set, Sorter.test_set = node.processor._dataset()
		# print(Sorter.temp_model)

	@staticmethod
	def _model(layers):
		for layer in layers:
			if layer != None:
				Net.model.append(layer)
		return Net().to(device)

	# THE PROBLEM IS RIGHT BELOW
	def sort(self, layers):
		# print(layers)
		# print('====')
		# print(Sorter.temp_model)

		# c_ind = Sorter.temp_model[0]
		c_ind = Sorter.indicator
		ci = 1

		# for layer in layers:
		# 	for _layer in layers:
		# 		if layer[1] == _layer[0]:
		# 			Sorter.temp_model.insert(ci, layer[1].algorithm())
		# 			ci += 1

		# SORTING ALGORITHM
		for layer in layers[1:]:
			if layer[0] == c_ind:
				Sorter.temp_model.insert(ci, layer[0])
				ci += 1
				c_ind = layer[1]

		# print(Sorter.temp_model)
		# print('===============')

		# MERGING ALGORITHM
		# temp_model = []
		# for layer in Sorter.temp_model:
		# 	temp_model = list(set(temp_model + layer))

		# print(temp_model)
		# print('====')

		#EXTRACTING LAYER OUT OF AN ARRAY OF LAYERS
		model = []
		for block in Sorter.temp_model:
			model.append(block.algorithm())
		# print(model)

		# return Sequential(*Sorter.temp_model), (Sorter.train_set, Sorter.test_set)
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
