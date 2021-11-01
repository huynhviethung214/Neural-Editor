import torch
import os
import numpy as np
# import matplotlib.pyplot as plt
import torchvision
from PIL import Image
# from torch.autograd import Variable
# from math import floor

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')


class ImageProcessor:
    def __init__(self, properties=None, **kwargs):
        self.properties = properties
        self.l2i = {}
        self.path_labels = properties['fpath']

        self.label2index(os.listdir(self.path_labels))

    def label2index(self, labels):
        for i, label in enumerate(sorted(labels)):
            self.l2i.update({label: i})

    @staticmethod
    def preprocessing(size, im):
        transform = torchvision.transforms.Compose([
            torchvision.transforms.Resize(size)
        ])
        return transform(im)

    def dataset(self):
        dataset = []
        fpath = self.properties['output_file']

        try:
            return np.load(f'nn_processors\\datasets\\{fpath}\\{fpath}.npy', allow_pickle=True)

        except FileNotFoundError:
            # os.makedirs('D:\\Python Projects\\Project Alpha\\Neural Editor\\nn_processors\\datasets\\{0}'.format(self.properties['output_file']))
            folders = os.listdir(self.path_labels)

            for i in range(len(folders)):
                for label in folders:
                    path = os.path.join(self.path_labels, label)
                    # print(label)

                    for im in os.listdir(path):
                        im = Image.open(os.path.join(path, im))

                        im = self.preprocessing((
                            self.properties['width'],
                            self.properties['height']),
                            im
                        )

                        try:
                            im = np.reshape(im, (1,
                                                 self.properties['channels'],
                                                 self.properties['width'],
                                                 self.properties['height']))

                            # im = torch.from_numpy(im)
                            # im = im.type(torch.cuda.FloatTensor)

                            # label = torch.from_numpy(np.array([i]))
                            # print(len(self.path_labels))
                            y = np.eye(len(os.listdir(self.path_labels)))[self.l2i[label]]
                            # y = np.array([i])
                            # y = -np.ones(len(os.listdir(self.path_labels)))
                            # y[self.l2i[label]] = 0
                            # print(y)
                            # y = torch.from_numpy(y)
                            # y = y.type(torch.cuda.FloatTensor)

                            # print(type(im))
                            # print(type(one_hot))
                            # im = Variable(im).to(device)
                            # one_hot = Variable(one_hot).to(device)
                            dataset.append([im, y])

                        except Exception as e:
                            continue

            if self.properties['shuffle']:
                for i in range(1000):
                    np.random.shuffle(dataset)

            # ratio = int(floor(len(dataset) * self.properties['split']))
            # train_set = np.asarray(dataset[:ratio])
            # test_set = np.asarray(train_set[ratio:])

            try:
                np.save(f'nn_processors\\datasets\\{fpath}\\{fpath}.npy', dataset)

            except FileNotFoundError:
                os.makedirs(f'nn_processors\\datasets\\{fpath}')

            return dataset


class BinaryProcessor(object):
    def __init__(self, properties=None, **kwargs):
        self.properties = properties

    def dataset(self):
        dataset = []
        fpath = self.properties['fpath']
        fname = fpath.split('\\')[-1].split('.')[0]

        try:
            return np.load(f'nn_processors\\datasets\\{fname}\\{fname}.npy', allow_pickle=True)

        except FileNotFoundError:
            with open(self.properties['fpath'], 'r') as f:
                for line in f.readlines():
                    binaries, dec = line.split(' ')
                    X = np.array(list(binaries), np.float64)
                    y = np.zeros((10), np.float64)
                    y[int(dec)] = 1

                    dataset.append([X, y])

            try:
                np.save(f'nn_processors\\datasets\\{fname}\\{fname}.npy', dataset)

            except FileNotFoundError:
                os.makedirs(f'nn_processors\\datasets\\{fname}')
                np.save(f'nn_processors\\datasets\\{fname}\\{fname}.npy', dataset)

        return dataset


# print(len(os.listdir('D:\\Python Projects\\Project Alpha\\SICR\\images')))

# props = {
#     'width': 28,
#     'height': 28,
#     'channels': 1,
#     'output_file': 'alphabets_dataset',
#     'shuffle': True,
#     'dataset': 'G:\\My Drive\\Neural Editor\\dataset'
# }
#
# dataset = ImageProcessor(properties=props).dataset()

# for X, y in dataset:
#     print(X)
#     print(y)
#     print(y.shape)
#     break

# _train_set, _test_set = processor._dataset()
# print(_train_set.size)
# for (im, label) in _train_set:
# 	_im = im.view(300, 300, 3)
# 	_im = _im.cpu().numpy().astype(np.uint8)
# 	_im = Image.fromarray(_im, 'RGB')
# 	_im.save('test.png')
# 	print(im.size())
# 	break
