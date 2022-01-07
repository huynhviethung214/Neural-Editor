import torch
import os
import numpy as np
import torchvision.datasets as datasets

from os.path import exists
from PIL import Image
from os.path import exists

# device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

kwargs = {
    'VAE': {
        'split': 0.3,
        'shuffle': True,
        'width': 28,
        'height': 28,
        'channels': 1,
        'output_file': 'mnist_dataset'
    }
}


class VAE:
    def __init__(self, properties=None, **kwargs):
        self.properties = properties

    def dataset(self):
        is_downloading = False
        fpath = self.properties['output_file']
        path = f'nn_processors\\datasets\\{fpath}'

        if not exists(path):
            os.makedirs(path)
            is_downloading = True

        dataset = datasets.MNIST(root=path,
                                 train=True,
                                 download=is_downloading)

        # DataLoader is used to load the dataset
        # for training
        loader = torch.utils.data.DataLoader(dataset=dataset,
                                             batch_size=64,
                                             shuffle=True)

        return loader
