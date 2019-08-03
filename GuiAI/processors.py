import torch
import numpy as np
from PIL import Image
import os
from math import floor
import matplotlib.pyplot as plt


class ImageProcessor(object):
	def __init__(self, **kwargs):
		self.properties = {'dataset': kwargs['dataset'],
						   'split_ratio': kwargs['split_ratio'],
						   'shuffle': kwargs['shuffle'],
						   'width': kwargs['width'],
						   'height': kwargs['height'],
						   'n_channels': kwargs['n_channels']}

	def _dataset(self):
		sub_dataset = []
		dataset = []

		for i, _dir in enumerate(os.listdir(self.properties['dataset'])):
			_path = self.properties['dataset'] + '\\{0}'.format(_dir)
			for im in os.listdir(_path):
				try:
					__path = _path + '\\{0}'.format(im)

					im = Image.open(__path)
					im = im.resize((self.properties['width'],
									self.properties['height']))
					im = np.array(im)
					im = torch.from_numpy(im)
					im = im.view(1, self.properties['n_channels'],
									self.properties['width'],
									self.properties['height'])

					label = torch.from_numpy(np.array([i]))
					label = label.type(torch.cuda.FloatTensor)
					im = im.type(torch.cuda.FloatTensor)

					sub_dataset.append([im, label])

					if self.properties['shuffle']:
						np.random.shuffle(sub_dataset)
				
				except OSError:
					pass

		ratio = int(floor(len(sub_dataset) * self.properties['split_ratio']))
		_train_set = np.asarray(sub_dataset[:ratio])
		_test_set = np.asarray(sub_dataset[ratio:])
		return _train_set, _test_set

# processor = ImageProcessor(width=300,
# 						   height=300,
# 						   split_ratio=0.8,
# 						   shuffle=True,
# 						   n_channels=3,
# 						   dataset='test_set')

# _train_set, _test_set = processor._dataset()
# print(_train_set.size)
# for (im, label) in _train_set:
# 	_im = im.view(300, 300, 3)
# 	_im = _im.cpu().numpy().astype(np.uint8)
# 	_im = Image.fromarray(_im, 'RGB')
# 	_im.save('test.png')
# 	print(im.size())
# 	break