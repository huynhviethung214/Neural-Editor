class BaseAlgorithm:
	def __init__(self, properties=None, **kwargs):
		self.properties = properties

	def load_algorithm(self):
		with open(self.properties['file_path'], 'r') as f:
			code = f.read()

		return self.properties, code
