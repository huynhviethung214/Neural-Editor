import json
import importlib

# from nn_modules.node import Node
# from nn_modules.nn_nodes import LinearNode, _XConv2dNode
# from utility.functions import _FlattenLayer
from nn_modules.base_component import Component

import nn_modules.nn_nodes


def generate_nn_components():
    importlib.reload(nn_modules.nn_nodes)

    with open('nn_modules\\nn_nodes.json', 'r') as f:
        nodes = json.load(f)

        for node_name in nodes.keys():
            if node_name not in globals():
                module = __import__('nn_modules.nn_nodes',
                                    fromlist=[node_name + 'Node'])
                _class = getattr(module, node_name + 'Node')
                # print(_class)

                globals()[node_name] = type(node_name,
                                            (Component,),
                                            {})

                globals()[node_name].attachment = _class
                globals()[node_name].text = node_name


generate_nn_components()

# class Linear(Component):
# 	def add_properties(self):
# 		self._attachment = LinearNode
# 		self.text = 'Linear'


# class XConv2d(Component):
# 	def add_properties(self):
# 		self._attachment = _XConv2dNode
# 		self.text = 'XConv2d'


# class ImageDataProcessor(Component):
# 	def add_properties(self):
# 		self._attachment = _ImageDataProcessor
# 		self.text = 'Image Processor'


# class Flatten(Component):
# 	def add_properties(self):
# 		self._attachment = _FlattenLayer
# 		self.text = 'Flatten'
