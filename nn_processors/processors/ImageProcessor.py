import torch
import os
import numpy as np
import torchvision

from PIL import Image
from os.path import exists

# device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

kwargs = {
    'ImageProcessor': {
        'fpath': 'D:\\Python Projects\\Project Alpha\\S&U\\PyTorch\\TreeRecognition\\test_set',
        'split': 0.3,
        'shuffle': True,
        'width': 300,
        'height': 300,
        'channels': 3,
        'output_file': 'tree_dataset'
    }
}


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
            folders = os.listdir(self.path_labels)

            # for i in range(len(folders)):
            #     for label in folders:
            #         path = os.path.join(self.path_labels, label)
            #
            #         for im in os.listdir(path):
            #             im = Image.open(os.path.join(path, im))
            #
            #             im = self.preprocessing((
            #                 self.properties['width'],
            #                 self.properties['height']),
            #                 im
            #             )
            #
            #             try:
            #                 im = np.reshape(im, (1,
            #                                      self.properties['channels'],
            #                                      self.properties['width'],
            #                                      self.properties['height']))
            #
            #                 y = np.array([i])
            #                 # y = np.eye(len(os.listdir(self.path_labels)))[self.l2i[label]]
            #                 # print(y.shape)
            #                 # y = np.reshape(y, (1, 6))
            #                 # print(y)
            #
            #                 dataset.append([im, y])
            #
            #             except Exception as e:
            #                 continue

            for i, name in enumerate(folders):
                path = f'{self.path_labels}\\{name}'
                for im in os.listdir(path):
                    try:
                        path = f'{path}\\{im}'
                        im = Image.open(path)
                        im = im.resize((self.properties['width'],
                                        self.properties['height']))
                        im = np.array(im)

                        if im.shape == ((self.properties['width'],
                                         self.properties['height'],
                                         (self.properties['channels']))):
                            label = np.array([i])
                            dataset.append([im, label])

                    except Exception as e:
                        pass

            if self.properties['shuffle']:
                for i in range(1000):
                    np.random.shuffle(dataset)

            path = f'nn_processors\\datasets\\{fpath}'

            if not exists(path):
                os.makedirs(f'nn_processors\\datasets\\{fpath}')
            np.save(f'nn_processors\\datasets\\{fpath}\\{fpath}.npy', dataset)

            # try:
            #     np.save(f'nn_processors\\datasets\\{fpath}\\{fpath}.npy', dataset)
            #
            # except FileNotFoundError:
            #     os.makedirs(f'nn_processors\\datasets\\{fpath}')

            return dataset
