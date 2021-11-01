from torch.nn import Module, Sequential
from torch.tensor import Tensor
from torch.autograd import grad, Variable
from torch.utils.data import Dataset, DataLoader
from torchvision.datasets import ImageFolder
from PIL import Image
import numpy as np
import torch
import os


class ImageProcessor(object):
	def __init__(self, **kwargs):
		self.dataset = kwargs['dataset'] + '\\{0}'
		self.split_ratio = kwargs['split_ratio']
		self.shuffle = kwargs['shuffle']
		self.default_size = kwargs['default_size']
		self.n_channels = kwargs['n_channels']
		self.labels = {}

	def _labels(self):
		for i, label in enumerate(os.listdir(self.dataset)):
			label = label.split('\\')[-1]
			self.labels.update({i: label})

	def dataset(self):
		sub_dataset = []
		dataset = []

		for i, _dir in enumerate(os.listdir(self.dataset)):
			for im in os.listdir(self.dataset.format(_dir)):
				_path = self.dataset.format(_dir) + '\\{0}'.format(im)
				
				im = Image.open(im)
				im = im.resize(self.default_size)
				im = np.array(im)
				im = torch.from_numpy(im)

				label = torch.from_numpy(np.array([i]))
				label = label.type(torch.cuda.FloatTensor)
				im = im.type(torch.cuda.FloatTensor)

				sub_dataset.append([im, label])

			ratio = int(floor(len(sub_dataset) * self.split_ratio))
			dataset.append(sub_dataset.split(ratio))
		return dataset


class NNet(Module):
	def __init__(self, model=None, **kwargs):
		self.model = Sequential(*model)

	def forward(self, x):
		out = self.model(x)
		return out
