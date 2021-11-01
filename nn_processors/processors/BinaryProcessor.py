import os
import numpy as np

kwargs = {
    'BinaryProcessor': {
        'fpath': 'test_set\\binary_dataset.txt'
    }
}


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
                    y = np.zeros(10, np.float64)
                    y[int(dec)] = 1

                    dataset.append([X, y])

            try:
                np.save(f'nn_processors\\datasets\\{fname}\\{fname}.npy', dataset)

            except FileNotFoundError:
                os.makedirs(f'nn_processors\\datasets\\{fname}')
                np.save(f'nn_processors\\datasets\\{fname}\\{fname}.npy', dataset)

        return dataset
