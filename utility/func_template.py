class Template:
	prop_dict = {}

	def __init__(self, **kwargs):
		for k in kwargs.keys():
			setattr(self, k, kwargs.get(k))

	def algorithm(self, params=None, _type=0):
		if _type == 0:
			if 'params' in self.prop_dict.keys():
				self.prop_dict['params'] = params

			return self.alg(**self.prop_dict)

		elif _type == 1:
			return self.alg(properties=self.prop_dict).dataset()
		
		elif _type == 2:
			return self.alg(properties=self.prop_dict).load_algorithm()
		
		elif _type == 3:
			return self.alg(properties=self.prop_dict).load_algorithm()

	def __str__(self):
		return self.name