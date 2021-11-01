import json
import importlib

from nn_modules.node import Node
# from nn_modules.base_node import BaseNode


# from torch.nn import ReLU, BatchNorm2d, Conv2d, MaxPool2d, Linear, Sequential


def generate_nn_nodes():
    with open('nn_modules\\nn_nodes.json', 'r') as f:
        nodes = json.load(f)

        for node_name in nodes.keys():
            _name = node_name + 'Node'

            if _name not in globals():
                # print(f'algorithms.{node_name}')
                module = __import__(f'algorithms.{node_name}',
                                    fromlist=['algorithm'])
                algo = getattr(module, 'algorithm')
                # print(algo)

                globals()[_name] = type(_name,
                                        (Node,),
                                        {})
                # node = Node()
                # node.node_template = nodes[node_name]
                # node.name = node_name
                # node.node_type = nodes[node_name]['node_type']
                # node.algorithm = algo

                globals()[_name].node_template = nodes[node_name]
                globals()[_name].name = node_name
                globals()[_name].node_type = nodes[node_name]['node_type']
                globals()[_name].algorithm = algo
                # globals()[_name].node_name = node_name


generate_nn_nodes()

# class LinearNode(Node):
# 	def add_components(self):
# 		self.set_id(link_type='Linear', _self=self)
# 		self.add_id()
# 		self.add_drop_down_list()
# 		self.add_val_input('n_in', INT_CODE)
# 		self.add_val_input('n_out', INT_CODE)
# 		self.add_list_data('bias', [True, False], BOOL_CODE)

# 	def algorithm(self):
# 		return Linear(self.properties['n_in'][1],
# 					  self.properties['n_out'][1],
# 					  self.properties['bias'][1])


# class _XConv2dNode(Node):
# 	def add_components(self):
# 		self.set_id(link_type='XConv2d', _self=self)
# 		self.add_id()
# 		self.add_drop_down_list()
# 		self.add_val_input('n_in', INT_CODE)
# 		self.add_val_input('n_out', INT_CODE)
# 		self.add_val_input('f_size', INT_CODE)
# 		self.add_val_input('stride', INT_CODE)
# 		self.add_val_input('padding', INT_CODE)
# 		self.add_val_input('b_norm', INT_CODE)
# 		self.add_val_input('mpk_size', INT_CODE)
# 		self.add_val_input('mp_stride', INT_CODE)

# 	def algorithm(self):
# 		n_in = self.properties['n_in'][1]
# 		n_out = self.properties['n_out'][1]
# 		f_size = self.properties['f_size'][1]
# 		stride = self.properties['stride'][1]
# 		padding = self.properties['padding'][1]
# 		b_norm = self.properties['b_norm'][1]
# 		mpk_size = self.properties['mpk_size'][1]
# 		mp_stride = self.properties['mp_stride'][1]

# 		return Sequential(
# 			Conv2d(in_channels=n_in, out_channels=n_out, kernel_size=f_size, stride=stride, padding=padding),
# 			BatchNorm2d(b_norm),
# 			ReLU(),
# 			MaxPool2d(kernel_size=mpk_size, stride=mp_stride)
# 		)
