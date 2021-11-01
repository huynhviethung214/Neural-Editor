import torch
from torch.nn import Module, ModuleDict
from queue import Queue, PriorityQueue
from Net.Net import Net

device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')


class Sorter:
    def sort(self, layers):
        # print(layers)
        node_names = []
        node_layers = []

        for layer in layers:
            for node in layer:
                if node.name not in node_names:
                    node_layers.append(node.algorithm())
                    node_names.append(node.name)

        return self._model(layers=node_layers, block_names=node_names)

    @staticmethod
    def _model(layers, block_names):
        model = []

        for layer in layers:
            if layer is not None:
                model.append(layer)

        # print(model)
        return Net(block_names=block_names,
                   model=model).to(device)


def get_obj(hierarchy=None, widget_name='', condition=None):
    for w in hierarchy.walk_reverse(loopback=True):
        if widget_name.lower() == str(w).split(' ')[0].split('.')[-1].lower():
            if not condition:
                return w
            
            else:
                for key in condition.keys():
                    if key in dir(w) and getattr(w, key) == condition[key]:
                        return w

# class LinksManager():
# 	def __init__(self):
# 		self.objs_list = {}

# 	def register_obj(self, name, obj):
# 		self.objs_list.update({name: obj})

# 	def remove_obj(self, name):
# 		self.objs_list.remove(name)

# 	def get_obj(self, name):
# 		return self.objs_list[name]
