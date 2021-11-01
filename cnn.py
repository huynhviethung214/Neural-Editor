from torch.nn import MaxPool2d, BatchNorm2d, \
                    Conv2d, Linear, Dropout,\
                    Module, Sequential, BCELoss, Sigmoid, CrossEntropyLoss
import torch
from torch.optim import Adam
import numpy as np
import os
import os.path as path
from PIL import Image


class ConvNet(Module):
    def __init__(self, in_channels, out_channels, kernel_size=(5, 5), stride=(1, 1)):
        super(ConvNet, self).__init__()
        self.convblock = Sequential(
            Conv2d(in_channels=in_channels,
                   out_channels=out_channels,
                   kernel_size=kernel_size,
                   stride=stride),
            BatchNorm2d(out_channels),
            MaxPool2d((2, 2)),
            Dropout(0.5)
        )

    def forward(self, x):
        return self.convblock(x)


class CNN(Module):
    def __init__(self):
        super(CNN, self).__init__()
        self.c1 = ConvNet(3, 16)
        self.c2 = ConvNet(16, 32)
        self.c3 = ConvNet(32, 64)
        self.c4 = ConvNet(64, 128)
        self.c5 = ConvNet(128, 64)

        # print(self.c5(self.c4(self.c3(self.c2(self.c1(x))))).shape)

        self.dense1 = Linear(64 * 5 * 5, 4)
        self.sigmoid = Sigmoid()

    def forward(self, x):
        x = self.c5(self.c4(self.c3(self.c2(self.c1(x)))))
        x = x.view(-1)

        return self.dense1(x)


def data_from_archive(fpath='D:\Python Projects\Project Alpha\dataset\Animals\custom'):
    # labels = np.eye(len(os.listdir(fpath)))
    dataset = []

    for i, category in enumerate(os.listdir(fpath)):
        ims_path = path.join(fpath, category)

        for im in os.listdir(ims_path):
            np_im = Image.open(path.join(ims_path, im))
            np_im = np_im.resize((300, 300))
            np_im = np.array(np_im)
            np_im = np_im.reshape((1, 3, 300, 300))
            # label = np.array([i])

            dataset.append([np_im, i])

    np.save('D:\Python Projects\Project Alpha\dataset\Animals\CNN.npy', dataset)

    return dataset


device = torch.device('cuda')
model = CNN().to(device)

# x = torch.cuda.FloatTensor(np.random.random((1, 3, 300, 300)))
# print(cnn(x))

if not path.exists('D:\Python Projects\Project Alpha\dataset\Animals\CNN.npy'):
    dataset = data_from_archive()

else:
    dataset = np.load('D:\Python Projects\Project Alpha\dataset\Animals\CNN.npy',
                      allow_pickle=True)


if not path.exists('D:\Python Projects\Project Alpha\dataset\Animals\CNN.model'):
    criterion = CrossEntropyLoss().to(device)
    optimizer = Adam(params=model.parameters(), lr=0.01)

    epochs = 100

    for _ in range(10):
        np.random.shuffle(dataset)

    for epoch in range(epochs):
        for (x, y) in dataset:
            x = torch.cuda.FloatTensor(x).to(device)
            y = torch.cuda.LongTensor(np.array([y])).to(device)

            out = model(x).to(device)
            out = out.reshape(1, 4)
            # print(out.shape, y.shape, y)
            loss = criterion(out, y)

            model.zero_grad()
            loss.backward()
            optimizer.step()

            # print(loss.data.item(), out.cpu().detach().numpy())
            # print(y.data.cpu().numpy(), out.data.cpu().numpy())

            print(f'Epoch: {epoch + 1}/{epochs} | Loss: {round(loss.data.item(), 2)} | '
                  f'Prediction - Expected: {torch.argmax(out).data.cpu().numpy()} / {y.item()} \n')

    torch.save(model.state_dict(), 'D:\Python Projects\Project Alpha\dataset\Animals\CNN.model')
    torch.cuda.empty_cache()

else:
    state_dict = torch.load('D:\Python Projects\Project Alpha\dataset\Animals\CNN.model')
    model.load_state_dict(state_dict)
    correct = 0

    # Load Image
    validate_path = 'D:\Python Projects\Project Alpha\dataset\Animals\\validate'
    if not path.exists('D:\Python Projects\Project Alpha\dataset\Animals\\validate_cnn.npy'):
        dataset = data_from_archive(validate_path)
        np.save('D:\Python Projects\Project Alpha\dataset\Animals\\validate_cnn.npy', dataset)
    else:
        dataset = np.load('D:\Python Projects\Project Alpha\dataset\Animals\\validate_cnn.npy',
                          allow_pickle=True)

    for _ in range(10):
        np.random.shuffle(dataset)

    for (x, y) in dataset:
        x = torch.cuda.FloatTensor(x).to(device)

        out = model(x).to(device)

        print(f'Prediction: {torch.argmax(out).data.cpu().numpy()} - Expected: {y}')

        if int(round(float(torch.argmax(out).data.cpu().numpy()), 0)) == int(y):
            correct += 1

    print(f'Accuracy: {(correct / len(dataset)) * 100}')
    print(f'Number Of Unseen Images: {len(dataset)}')

