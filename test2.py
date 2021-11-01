# from kivy.uix.modalview import ModalView
# from kivy.uix.boxlayout import BoxLayout
# from kivy.uix.label import Label
# from kivy.app import App
#
#
# class a(ModalView):
# 	def __init__(self, **kwargs):
# 		super(a, self).__init__()
# 		self.size_hint = (None, None)
# 		self.size = (400, 400)
# 		# self.pos_hint = {'x': 100, 'y': 50}
# 		# self.pos = (100, 100)
# 		self.add_widget(Label(text='Hello world'))
#
#
# class b(App):
# 	def build(self):
# 		c = BoxLayout()
# 		c.bind(on_touch_up=self.open_popup)
# 		# a().open()
# 		return c
#
# 	def open_popup(self, obj, touch):
# 		a().open()
#
#
# if __name__ == '__main__':
# 	b().run()

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision
from torch.autograd import Variable

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")


# print(device)


class CNN(nn.Module):
    def __init__(self, num_classes=26):
        super(CNN, self).__init__()
        self.flattened = None
        
        self.layer1 = nn.Sequential(
            nn.Conv2d(1, 16, kernel_size=5, stride=1, padding=2),
            nn.BatchNorm2d(16),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2))
        
        self.layer2 = nn.Sequential(
            nn.Conv2d(16, 32, kernel_size=5, stride=1, padding=2),
            nn.BatchNorm2d(32),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2))
        
        self.layer3 = nn.Sequential(
            nn.Conv2d(32, 64, kernel_size=5, stride=1, padding=2),
            nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2))
        
        self.layer4 = nn.Sequential(
            nn.Conv2d(64, 128, kernel_size=5, stride=1, padding=2),
            nn.BatchNorm2d(128),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2))
        
        x = torch.randn(28, 28).view(-1, 1, 28, 28)
        self.convs(x)
        
        # self.flatten = nn.Flatten()
        
        # x = torch.randn(1, 128)
        self.fc1 = nn.Linear(self.flattened, 512)
        # x = self.fc1(x)
        # print(x.shape)
        self.fc2 = nn.Linear(512, num_classes)
    
    def convs(self, x):
        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        x = self.layer4(x)
        
        if self.flattened == None:
            self.flattened = x.view(x.size(0), -1).shape[1]
        # print(self.flattened)
        
        return x
    
    def forward(self, x):
        # print(x.shape)
        x = self.convs(x)
        # print(x.shape)
        x = x.view(x.size(0), -1)
        # print(x.shape)
        x = self.fc1(x)
        x = self.fc2(x)
        
        return F.softmax(x, dim=1)


# import os
# path = 'D:\\Python Projects\\Project Alpha\\SICR\\images'
# for data in os.listdir(path):
#     print(len(os.listdir(os.path.join(path, data))))


dataset = np.load('/\\nn_processors\\datasets\\'
                  'alphabets_dataset\\dataset1.npy',
                  allow_pickle=True)


import cv2
import os
from PIL import Image
from matplotlib import pyplot as plt

data = None
Y = None
X = None
np.random.shuffle(dataset)
for x, y in dataset:
    X = x
    data = torch.Tensor(x).cpu().view(1, 28, 28).permute(1, 2, 0)
    Y = y

plt.imshow(data)
plt.show()
l2i = []

for label in sorted(os.listdir('D:\\Python Projects\\'
							   'Project Alpha\\SICR\\images')):
    l2i.append(label)

model = CNN().to(device)

model.load_state_dict(torch.load('D:\\Python Projects\\'
                                 'Project Alpha\\Neural Editor\\model.pt'))
# print(model)
model.eval()

X = Variable(torch.Tensor(X).view(-1, 1, 28, 28)).to(device)

out = model(X)
print(Y)
print(l2i[torch.argmax(out).item()])


# X_set = torch.Tensor([i[0] for i in dataset]).view(-1, 28, 28)
# Y_set = torch.Tensor([i[1] for i in dataset])
# print(len(X_set), len(Y_set))

def train_and_eval():
    cnn = CNN().to(device)
    # print(cnn)
    BATCH_SIZE = 2048
    loss_func = nn.BCEWithLogitsLoss()
    optimizer = torch.optim.Adam(cnn.parameters(), lr=0.001)
    # loss = 0
    
    for epoch in range(5):
        for i in range(0, len(dataset), BATCH_SIZE):
            image = Variable(X_set[i:i + BATCH_SIZE].view(-1, 1, 28, 28)).to(device)
            label = Variable(Y_set[i:i + BATCH_SIZE]).to(device)
            
            optimizer.zero_grad()
            out = cnn(image)
            # print(out.shape)
            # print(label.shape)
            label = label.view(-1, 26)
            # print(label.shape)
            
            loss = loss_func(out, label).to(device)
            loss.backward()
            optimizer.step()
            
        print('Epoch: {epoch}, Loss: {loss}'.format(loss=loss,
                                                    epoch=epoch,
                                                    n_data=len(dataset)))
    
    cnn.eval()
    correct = 0
    total = 0
    
    with torch.no_grad():
        for epoch in range(5):
            for i in range(0, len(dataset), BATCH_SIZE):
                X = Variable(X_set[i:i + BATCH_SIZE].view(-1, 1, 28, 28)).to(device)
                y = Variable(Y_set[i:i + BATCH_SIZE]).to(device)
                
                optimizer.zero_grad()
                out = cnn(X)
            
                real_class = torch.argmax(y.cpu())
                predicted_class = torch.argmax(out)
                
                if predicted_class == real_class:
                    correct += 1
                total += 1
        
        print('Accuracy-->{acc}'.format(acc=(correct / total) * 100))
    
    torch.save(cnn.state_dict(), 'model.pt')


# train_and_eval()

