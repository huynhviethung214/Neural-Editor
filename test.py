# # import torch
# # import os
# # import numpy as np
# # import matplotlib.pyplot as plt
# # import torchvision
# # from PIL import Image
# # from torch.nn import Conv2d, Linear, BatchNorm2d, Module, ReLU, Sequential, MaxPool2d, CrossEntropyLoss
# # from torch.autograd import Variable
# # from math import floor
# # import random
#
# # device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
#
#
# # class _ImageProcessor(object):
# # 	def __init__(self, **kwargs):
# # 		self.properties = {'dataset': 'D:\\Python Projects\\Project Alpha\\test_set',
# # 						   'split': 0.5,
# # 						   'shuffle': True,
# # 						   'width': 300,
# # 						   'height': 300,
# # 						   'z': 3}
#
# # 	def preprocessing(self, size, im):
# # 		transform = torchvision.transforms.Compose([
# # 			torchvision.transforms.Resize(size)
# # 		])
# # 		return transform(im)
#
# # 	def _dataset(self):
# # 		sub_dataset = []
# # 		dataset = []
# # 		path = self.properties['dataset']
#
# # 		for i, _dir in enumerate(os.listdir(path)):
# # 			_path = path + '\\{0}'.format(_dir)
# # 			for im in os.listdir(_path):
# # 				try:
# # 					__path = _path + '\\{0}'.format(im)
#
# # 					im = Image.open(__path)
# # 					im = self.preprocessing((
# # 						self.properties['width'],
# # 						self.properties['height']),
# # 						im
# # 					)
#
# # 					im = np.reshape(im, (1, self.properties['z'],
# # 										self.properties['width'],
# # 										self.properties['height']))
#
# # 					im = torch.from_numpy(im)
# # 					im = im.type(torch.cuda.FloatTensor)
#
# # 					label = torch.from_numpy(np.array([i]))
# # 					label = label.type(torch.cuda.LongTensor)
# # 					# print(label)
#
# # 					im = Variable(im).to(device)
# # 					label = Variable(label).to(device)
#
# # 					sub_dataset.append([im, label])
#
# # 				except OSError:
# # 					pass
#
# # 		if self.properties['shuffle']:
# # 			for i in range(10):
# # 				np.random.shuffle(np.array(sub_dataset))
#
# # 		ratio = int(floor(len(sub_dataset) * self.properties['split']))
# # 		_train_set = np.asarray(sub_dataset[:ratio])
# # 		_test_set = np.asarray(sub_dataset[ratio:])
#
# # 		return _train_set, _test_set
#
# # a = _ImageProcessor()
# # b, c = a._dataset()
#
# # class NN(Module):
# #     def __init__(self):
# #         super(NN, self).__init__()
# #         self.layer1 = Sequential(
# #             Conv2d(3, 16, kernel_size=5, stride=1, padding=2),
# #             BatchNorm2d(16),
# #             ReLU(),
# #             MaxPool2d(kernel_size=2, stride=2))
#
# #         self.layer2 = Sequential(
# #             Conv2d(16, 32, kernel_size=5, stride=1, padding=2),
# #             BatchNorm2d(32),
# #             ReLU(),
# #             MaxPool2d(kernel_size=2, stride=2))
#
# #         self.layer3 = Sequential(
# #             Conv2d(32, 64, kernel_size=5, stride=1, padding=2),
# #             BatchNorm2d(64),
# #             ReLU(),
# #             MaxPool2d(kernel_size=2, stride=2))
#
# #         self.layer4 = Sequential(
# #             Conv2d(64, 128, kernel_size=5, stride=1, padding=2),
# #             BatchNorm2d(128),
# #             ReLU(),
# #             MaxPool2d(kernel_size=2, stride=2))
#
# #         self.layer5 = Sequential(
# #             Conv2d(128, 64, kernel_size=5, stride=1, padding=2),
# #             BatchNorm2d(64),
# #             ReLU(),
# #             MaxPool2d(kernel_size=2, stride=2))
#
# #         self.layer6 = Sequential(
# #             Conv2d(64, 32, kernel_size=5, stride=1, padding=2),
# #             BatchNorm2d(32),
# #             ReLU(),
# #             MaxPool2d(kernel_size=2, stride=2))
#
# #         self.fc = Linear(512, 2)
#
# #     def forward(self, x):
# #         out = self.layer1(x)
# #         out = self.layer2(out)
# #         out = self.layer3(out)
# #         out = self.layer4(out)
# #         out = self.layer5(out)
# #         out = self.layer6(out)
# #         out = out.view(-1, 512)
# #         out = self.fc(out)
# #         return out
#
# # model = NN().to(device)
#
# # criterion = CrossEntropyLoss()
# # optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
#
# # for epoch in range(1, 10):
# # 	for i, (X, y) in enumerate(b):
# # 		output = model(X)
# # 		loss = criterion(output, y).to(device)
#
# # 		model.zero_grad()
# # 		loss.backward()
# # 		optimizer.step()
#
# # 		# if i % 100 == 0:
# # 		print('[{0}: {1}]-->[Prediction:{2} | Expected Prediction: {3}]'.format(epoch, loss, torch.argmax(output), y))
#
# # torch.save(model.state_dict(), 'model_weights.prmt')
#
# # from kivy.uix.button import Button
# # from kivy.uix.floatlayout import FloatLayout
# # from kivy.uix.label import Label
# # from kivy.app import App
#
#
# # class a(FloatLayout):
# # 	def __init__(self, **kwargs):
# # 		super(a, self).__init__()
# # 		button = Button(pos=(self.width/2, self.height/2),
# # 						size_hint=(0.3, 0.3))
# # 		button.bind(on_press=self.open_dropdown)
#
# # 		self.state = 0
# # 		self.add_widget(button)
#
# # 	def open_dropdown(self, obj):
# # 		# print(self.to_window(*obj.pos))
# # 		if self.state == 0:
# # 			self.add_widget(Button(size_hint=obj.size_hint,
# # 									pos=(obj.pos[0] + obj.width,
# # 										obj.pos[1])))
# # 			self.state = 1
#
# # 		elif self.state == 1:
# # 			self.remove_widget(self.children[0])
# # 			self.state = 0
#
#
# # class b(App):
# # 	def build(self):
# # 		return a()
#
#
# # if __name__ == '__main__':
# # 	b().run()
#
#
# # import cv2
#
# # cap = cv2.VideoCapture(0)
# # # cap.set(cv2.cv2.CV_CAP_PROP_FRAME_WIDTH, 640)
#
# # # cap.set(cv2.cv2.CV_CAP_PROP_FRAME_HEIGHT, 480)
# # ret, image = cap.read()
#
# # while True:
# # 	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# # 	cv2.imshow('Gray image', gray)
#
# # 	if cv2.waitKey(1) & 0xFF == ord('q'):
# # 		break
#
# # # image = cv2.imread('C:\\Users\\v3n0m\\OneDrive\\Pictures\\Camera Roll\\WIN_20210114_09_23_29_Pro.jpg')
# # cap.release()
# # # cv2.imshow('Original image',image)
#
# # # cv2.waitKey(0)
# # # cv2.destroyAllWindows()
#
# # import pyfirmata
# # import time
# #
# # if __name__ == '__main__':
# #     board = pyfirmata.Arduino('COM3')
# #     print("Communication Successfully started")
# #
# #     while True:
# #         board.digital[13].write(1)
# #         time.sleep(1)
# #         board.digital[13].write(0)
# #         time.sleep(1)
#
# # Arduino: 1.8.7 (Windows 10), Board: "Arduino/Genuino Uno"
#
# # Sketch uses 12470 bytes (38%) of program storage space. Maximum is 32256 bytes.
# # Global variables use 1065 bytes (52%) of dynamic memory, leaving 983 bytes for local variables. Maximum is 2048 bytes.
# # avrdude: ser_open(): can't open device "\\.\COM3": Access is denied.
#
#
# # Problem uploading to board.  See http://www.arduino.cc/en/Guide/Troubleshooting#upload for suggestions.
#
# # This report would have more information with
# # "Show verbose output during compilation"
# # option enabled in File -> Preferences.
#
# # from kivy.uix.dropdown import DropDown
# # from kivy.uix.button import Button
# # from kivy.base import runTouchApp
# #
# # dropdown = DropDown(auto_width=False)
# # for index in range(10):
# #
# #     btn = Button(text='Value %d' % index, size_hint_y=None, height=44, size_hint_x=None, width=200)
# #
# #     btn.bind(on_release=lambda btn: dropdown.select(btn.text))
# #     dropdown.add_widget(btn)
# # mainbutton = Button(text='Hello', size_hint=(None, None), pos=(100, 100))
# #
# # mainbutton.bind(on_release=dropdown.open)
# # dropdown.bind(on_select=lambda instance, x: setattr(mainbutton, 'text', x))
# #
# # if __name__ == '__main__':
# #     runTouchApp(mainbutton)
#
# # import matplotlib.pyplot as plt
# # plt.plot([1, 2, 3, 4])
# # plt.ylabel('some numbers')
# # plt.show()
#
# # code = '''
# # def f(x):
# # 	print(x)
# # '''
# #
# # exec(code)
# #
# # f(20)
#
# # class A:
# # 	def __init__(self):
# # 		self.prop = 10
# #
# # 	def a(self):
# # 		pass
# #
# # 	def c(self):
# # 		pass
# #
# # 	def b(self):
# # 		pass
# #
# #
# # aa = A()
# # print(dir(aa))
# # # print()
# # m = [func for func in dir(aa) if '__' not in func]
# #
# # print(m)
# #
# # condition = [0, 1][0 == 1]
# # print(condition)
#
# # import numpy as np
# # import torch
# # import torch.nn as nn
# # import torch.nn.functional as F
# # import torchvision
# # from torch.autograd import Variable
# #
# # device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
# # # print(device)
# #
# #
# # class CNN(nn.Module):
# #     def __init__(self, num_classes=26):
# #         super(CNN, self).__init__()
# #         self.flattened = None
# #
# #         self.layer1 = nn.Sequential(
# #             nn.Conv2d(1, 16, kernel_size=5, stride=1, padding=2),
# #             nn.BatchNorm2d(16),
# #             nn.ReLU(),
# #             nn.MaxPool2d(kernel_size=2, stride=2))
# #
# #         self.layer2 = nn.Sequential(
# #             nn.Conv2d(16, 32, kernel_size=5, stride=1, padding=2),
# #             nn.BatchNorm2d(32),
# #             nn.ReLU(),
# #             nn.MaxPool2d(kernel_size=2, stride=2))
# #
# #         self.layer3 = nn.Sequential(
# #             nn.Conv2d(32, 64, kernel_size=5, stride=1, padding=2),
# #             nn.BatchNorm2d(64),
# #             nn.ReLU(),
# #             nn.MaxPool2d(kernel_size=2, stride=2))
# #
# #         self.layer4 = nn.Sequential(
# #             nn.Conv2d(64, 128, kernel_size=5, stride=1, padding=2),
# #             nn.BatchNorm2d(128),
# #             nn.ReLU(),
# #             nn.MaxPool2d(kernel_size=2, stride=2))
# #
# #         x = torch.randn(28, 28).view(-1, 1, 28, 28)
# #         self.convs(x)
# #
# #         # self.flatten = nn.Flatten()
# #
# #         # x = torch.randn(1, 128)
# #         self.fc1 = nn.Linear(self.flattened, 512)
# #         # x = self.fc1(x)
# #         # print(x.shape)
# #         self.fc2 = nn.Linear(512, num_classes)
# #
# #     def convs(self, x):
# #         x = self.layer1(x)
# #         x = self.layer2(x)
# #         x = self.layer3(x)
# #         x = self.layer4(x)
# #
# #         if self.flattened == None:
# #             self.flattened = x.view(x.size(0), -1).shape[1]
# #             # print(self.flattened)
# #
# #         return x
# #
# #     def forward(self, x):
# #         # print(x.shape)
# #         x = self.convs(x)
# #         # print(x.shape)
# #         x = x.view(x.size(0), -1)
# #         # print(x.shape)
# #         x = self.fc1(x)
# #         x = self.fc2(x)
# #
# #         return F.softmax(x, dim=1)
# #
# # # import os
# # # path = 'D:\\Python Projects\\Project Alpha\\SICR\\images'
# # # for data in os.listdir(path):
# # #     print(len(os.listdir(os.path.join(path, data))))
# #
# #
# # dataset = np.load('D:\\Python Projects\\Project Alpha\\Neural Editor\\nn_processors\\datasets\\'
# #                   'alphabets_dataset\\dataset.npy',
# #                   allow_pickle=True)
# #
# # # import cv2
# # # from PIL import Image
# # # from matplotlib import pyplot as plt
# # #
# # # data = None
# # # Y = None
# # # X = None
# # #
# # # for x, y in dataset:
# # #     # pilTrans = torchvision.transforms.ToTensor()
# # #     X = x
# # #     data = x.cpu().view(1, 28, 28).permute(1, 2, 0)
# # #     Y = y
# # #     break
# # #
# # # print(Y)
# # # plt.imshow(data)
# # # plt.show()
# # #
# # # model = CNN().to(device)
# # #
# # # model.load_state_dict(torch.load('D:\\Python Projects\\'
# # #                                  'Project Alpha\\Neural Editor\\model1.pt'))
# # # # print(model)
# # # model.eval()
# # #
# # # X = Variable(X).to(device)
# # #
# # # out = model(X)
# # # print(out)
# #
# #
# # def train_and_eval():
# #     cnn = CNN().to(device)
# #     # print(cnn)
# #     loss_func = nn.BCEWithLogitsLoss()
# #     optimizer = torch.optim.Adam(cnn.parameters(), lr=0.001)
# #     # loss = 0
# #
# #     for i in range(5):
# #         for j, (image, label) in enumerate(dataset):
# #             image = Variable(image).to(device)
# #             label = Variable(label).to(device)
# #
# #             optimizer.zero_grad()
# #             out = cnn(image)
# #             # print(out.shape)
# #             # print(label.shape)
# #             label = label.view(-1, 26)
# #             # print(label.shape)
# #
# #             loss = loss_func(out, label).to(device)
# #             loss.backward()
# #             optimizer.step()
# #
# #             print('Epoch: {epoch}, {j}/{n_data} , Loss: {loss}'.format(loss=loss,
# #                                                                        epoch=i,
# #                                                                        j=j,
# #                                                                        n_data=len(dataset)))
# #
# #     cnn.eval()
# #     correct = 0
# #     total = 0
# #
# #     with torch.no_grad():
# #         for image, label in dataset:
# #             _image = Variable(image).to(device)
# #             _label = Variable(label).to(device)
# #
# #             result = cnn(_image)
# #             _, predicted = torch.max(result.data, 1)
# #             total += _label.size(0)
# #             # correct += (predicted == _label).sum()
# #             correct += ((predicted.data == _label.data).size(0))
# #
# #         print('Accuracy-->{acc}'.format(acc=(correct / total) * 100))
# #
# #     torch.save(cnn.state_dict(), 'model.pt')
# #
# # train_and_eval()
#
# # with open('algorithms\\Conv1D.py', 'r') as f:
# # 	code = '''class A: pass'''
# # 	ret = exec(code)
#
# # a = {2: 'A'}
# # print(a)
#
# # import numpy as np
# # print(np.array(list('01100'), dtype=np.float64))
# # print(np.fromstring('01010', np.float64))
# # a, b = '1 b'.split(' ')
# # print(a, b)
# # import os
# # fpath = 'nn_processors\\processors'
# #
# # for f in os.listdir(fpath):
# #     if '_' not in f:
# #         fname = f.split('.')[0]
# #         source = fpath.replace('\\', '.')
# #
# #         module = __import__(source + f'.{fname}', fromlist=[fname, 'args_list'])
# #         processor = getattr(module, f.split('.')[0])
# #         args = getattr(module, 'args_list')
#
# # import torch
# # import numpy as np
#
# # a = (torch.from_numpy(np.array([0, 0, 1, 1, 1, 1, 1])), torch.from_numpy(np.array([0, 0, 1, 1, 2, 1, 1])),)
# # a = (torch.from_numpy(np.array([0, 0, 1, 1, 1, 1, 1])),)
# # a = (*a,)
# # print(len(a))
#
# # print('LinearNode'[0:-4])
# # A = np.array([[1, 1],
# #               [1, 1]])
# # A = np.array([[2, 2],
# #               [3, -1]])
# # print(A + np.array([5]))
#
# # import GPUtil
# # from tabulate import tabulate
# #
# # print("="*40, "GPU Details", "="*40)
# # gpus = GPUtil.getGPUs()
# # list_gpus = []
# # for gpu in gpus:
# #     # get the GPU id
# #     gpu_id = gpu.id
# #     # name of GPU
# #     gpu_name = gpu.name
# #     # get % percentage of GPU usage of that GPU
# #     gpu_load = f"{gpu.load*100}%"
# #     # get free memory in MB format
# #     gpu_free_memory = f"{gpu.memoryFree}MB"
# #     # get used memory
# #     gpu_used_memory = f"{gpu.memoryUsed}MB"
# #     # get total memory
# #     gpu_total_memory = f"{gpu.memoryTotal}MB"
# #     # get GPU temperature in Celsius
# #     gpu_temperature = f"{gpu.temperature} °C"
# #     gpu_uuid = gpu.uuid
# #     list_gpus.append((
# #         gpu_id, gpu_name, gpu_load, gpu_free_memory, gpu_used_memory,
# #         gpu_total_memory, gpu_temperature, gpu_uuid
# #     ))
# # print(tabulate(list_gpus, headers=("id", "name", "load", "free memory", "used memory", "total memory", "temperature", "uuid")))
#
# # if __name__ == '__main__':
# #     from cpuinfo import get_cpu_info
# #     info = get_cpu_info()['brand_raw']
# #     print(info)
#
#
# # for i in range(len(a)):
# #     print(a[i])
#
# # print(torch.cat((a[0], a[1]), dim=-1).size())
#
# # def b(x):
# #     # x = (x)
# #     print(len(x))
# #
# #
# # b((a,))
#
# # print(len(a))
# # print(a)

import json
from settings.config import configs
# from settings import config
from importlib import reload
# # print(globals()['device'])
#
# # with open('settings/settings.json', 'w') as f:
# #     json.dump({'device': 'cuda:0'}, f)
#
# # reload(config)
# # __import__('settings.config')
# # print(globals()['device'])

# modules = __import__('settings.config')
# print(modules.config.device)
# modules.config.device = 'gpu'
#
# # reload(config)
# modules = __import__('settings.config')
# print(modules.config.device)

# print(configs['device'])
# # configuration.device = 'cpu'
# with open('settings/settings.json', 'w') as f:
#     json.dump({'device': 'cuda:0'}, f)
# configs.reload_config() # Apply settings
# print(configs['device'])
# print(configs.keys())
# a = [1, 2, 3, 4, 'cuda']

# print([i for i in range(10)])
# from settings.config import configs
# print(configs['device'])
#
# a = {}
# a['device']['name'] = '1'
# print(a)

# a = [[1, 2], [4, 5]]
# m = []
# n = []
#
# for b in a:
#     for c in b:
#         m.append(c)
#     n.append(m)
#     m = []
# print(n)


# class Node:
#     def __init__(self, data):
#         self.data = None
#         self.next = None
#
#
# class LinkedList:
#     def __init__(self):
#         self.head = Node(None)
#         self.tail = None
#
#         self.head.next = self.tail
#
#     def append(self, item):
#         self.head.next = item
#         item.next = self.tail
#
#     def locate(self, data):
#         current_node = self.head
#         index = 0
#
#         while current_node.next:
#             if current_node.data == data:
#                 break
#             index += 1
#             current_node = current_node.next
#         return index
#
#
# node1 = Node(10)
# node2 = Node(20)
# node3 = Node(30)
#
# ll = LinkedList()
# ll.append(node1)
# ll.append(node2)
# ll.append(node3)
#
# print(ll.locate(10))

# import torch
# import numpy as np

# _input = torch.randn(1, 6, requires_grad=True)
# target = torch.empty(1, dtype=torch.long).random_(5)
# print(torch.argmax(torch.from_numpy(np.array([1, 0, 0, 0, 0, 0]))))
# print(_input)

# print(np.array([10]).shape)
# print(torch.LongTensor(10))

# ll = LinkedList()
# ll.insertNode(2)
# ll.insertNode(4)
# ll.insertNode(5)
# ll.insertNode(6)
#
# ll.deleteList(4)
#
# ll.printList()

# from threading import Thread
#
# def a():
#     print('a1\n')
#
#
# jobs = []
# jobs.append(a)
#
#
# def process_jobs():
#     while True:
#         print('Runnning')
#         if len(jobs) > 0:
#             jobs[0]()
#             jobs.pop(0)
#
#
# thread = Thread(target=process_jobs, daemon=True)
# thread.start()
#
# jobs.append(a)
# jobs.append(a)
# jobs.append(a)
# print(len({'a', 'b', 'c'}))

# q1 = Queue()
# q1.enQueue(3)
# q1.enQueue(2)
# q1.enQueue(1)
#
# q2 = Queue()
# q2.enQueue(1)
# q2.enQueue(3)
# q2.enQueue(2)
#
# c = 0
#
# while not q1.is_empty():
#     # print(q1.data, q2.data)
#     if q1.get_val() != q2.get_val():
#         temp = q1.deQueue()
#         q1.enQueue(temp)
#
#     elif q1.get_val() == q2.get_val():
#         q1.deQueue()
#         q2.deQueue()
#
#     c += 1
#
# print(c)


# def map_properties(fn):
#     from functools import wraps
#     @wraps(fn)
#     def _map_properties(*args, **kwargs):
#         self = args[0]
#         a = fn(self)
#         return a, self.properties
#     return _map_properties
#
#
# class Conv2d:
#     def __init__(self):
#         self.properties = {
#             '1': 1,
#             '2': 2,
#             '3': 3,
#             '4': 4,
#         }
#
#     @map_properties
#     def alg(self):
#         func = object
#         return func
#
#
# conv2d = Conv2d()
# a, b = conv2d.alg()
# print(a, b)

# class BreakException(Exception):
#     def __str__(self):
#         return 'break'
#
#
# def break_loop(fn):
#     # from functools import wraps
#     # @wraps(fn)
#     def _break_loop(*args, **kwargs):
#         try:
#             fn()
#         except BreakException:
#             return None, None
#     return _break_loop
#
#
# def add_breaker():
#     raise BreakException
#
#
# def record(fn):
#     # from functools import wraps
#     # @wraps(fn)
#     def _record(*args, **kwargs):
#         v1, v2 = fn()
#     return _record
#
#
# @record
# @break_loop
# def a():
#     for i in range(10):
#         print(i)
#         add_breaker()
#
#     return 0, 0
#
#
# a()
