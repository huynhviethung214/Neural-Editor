import torch
import os
import numpy as np
import matplotlib.pyplot as plt
import torchvision
from PIL import Image
from torch.autograd import Variable
from math import floor

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')


class _ImageProcessor(object):
	def __init__(self, **kwargs):
		self.properties = {'dataset': None,
						   'split': None,
						   'shuffle': None,
						   'width': None,
						   'height': None,
						   'z': None}

	def preprocessing(self, size, im):
		transform = torchvision.transforms.Compose([
			torchvision.transforms.Resize(size)
		])
		return transform(im)

	def _dataset(self):
		sub_dataset = []
		dataset = []
		path = self.properties['dataset']

		for i, _dir in enumerate(os.listdir(path)):
			_path = path + '\\{0}'.format(_dir)
			for im in os.listdir(_path):
				try:
					__path = _path + '\\{0}'.format(im)

					im = Image.open(__path)
					im = self.preprocessing((
						self.properties['width'],
						self.properties['height']),
						im
					)

					im = np.reshape(im, (1, self.properties['z'],
										self.properties['width'],
										self.properties['height']))

					im = torch.from_numpy(im)
					im = im.type(torch.cuda.FloatTensor)

					label = torch.from_numpy(np.array([i]))
					label = label.type(torch.cuda.LongTensor)

					im = Variable(im).to(device)
					label = Variable(label).to(device)

					sub_dataset.append([im, label])

				except Exception:
					pass

		if self.properties['shuffle']:
			for i in range(10):
				np.random.shuffle(np.array(sub_dataset))

		ratio = int(floor(len(sub_dataset) * self.properties['split']))
		_train_set = np.asarray(sub_dataset[:ratio])
		_test_set = np.asarray(sub_dataset[ratio:])

		return (_train_set, _test_set)


class BinaryDataset(object):
	def __init__(self, **kwargs):
		pass

# processor = _ImageProcessor(width=300,
# 						    height=300,
# 						    split_ratio=0.8,
# 						    shuffle=True,
# 						    n_channels=3,
# 						    dataset='test_set')

# _train_set, _test_set = processor._dataset()
# print(_train_set.size)
# for (im, label) in _train_set:
# 	_im = im.view(300, 300, 3)
# 	_im = _im.cpu().numpy().astype(np.uint8)
# 	_im = Image.fromarray(_im, 'RGB')
# 	_im.save('test.png')
# 	print(im.size())
# 	break