import numpy as np


np.random.seed(100)

class Linear():
	def __init__(self, n_feature, n_label):
		super(Linear, self).__init__()
		self.w = np.random.rand(n_feature, n_label)
		self.b = np.random.rand(1, n_label)

		# print(self.w.shape)
		# print(self.b.shape)

	def model(self, x):
		return np.add(np.matmul(x, self.w), self.b)


x = np.array([[0, 0, 0],
			  [1, 0, 0],
			  [0, 0, 1],
			  [1, 1, 0],
			  [0, 1, 1]], dtype='float32')
# print(x.shape)

y = np.array([[0],
			  [4],
			  [1],
			  [6],
			  [3]], dtype='float32')
# print(y.shape)

linear = Linear(x.shape[1], y.shape[1])
pred = linear.model(x)
print(pred)

def mse():
	sst = 0

	for i in range(len(y)):
		# print(y[i])
		sst += np.square(y[i] - pred[i])

	return (1 / len(y)) * sst

print(mse())
