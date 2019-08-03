from node import Node


class LinearNode(Node):
	def add_components(self):
		self.set_id(_type='Linear', _self=self)
		self.add_id()
		self.add_drop_down_list()
		self.add_val_input('n_in', float)
		self.add_val_input('n_out', float)
		self.add_list_data('bias', [False, True])
