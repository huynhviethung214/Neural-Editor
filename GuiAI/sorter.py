class Sorter(object):
	temp_model = []

	@classmethod
	def setup(cls, layers):
		for layer in layers:
			for node in layer:
				if node._type == 0:
					cls.temp_model.insert(0, node)

				elif node._type == 2:
					cls.temp_model.insert(1, node)

	@classmethod
	def sort(cls, layers):
		ci = 0
		if len(layers) > 1:
			for layer in layers:
				if layer[0] == cls.temp_model[ci]:
					if layer[1]._type != 2:
						ci += 1
						cls.temp_model.insert(1, layer[1].algorithm())
		return cls.temp_model
