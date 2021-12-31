import torch


def evaluating_alg(self, properties):
	target = None
	pred = None

	with torch.no_grad():
		score = 0

		for epoch in range(properties['epochs']):
			for X, y in properties['dataset']:
				if self.end_task:
					print('End Task')
					return

				X = torch.Tensor(X)
				y = torch.Tensor(y)
				X = X.to(properties['device'])
				y = y.to(properties['device'])

				output = properties['model'](X).to(properties['device']).view(-1)
				pred = torch.argmax(output)

				target = y.tolist()[0]
				pred = pred.item()

			if target == pred:
				score += 1
