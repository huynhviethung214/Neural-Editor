import torch
from kivy.uix.popup import Popup
from kivy_garden.graph import Graph
from torch.nn import Module, ModuleDict

from queue import Queue, PriorityQueue
from functools import wraps

from Net.Net import Net
from graph.graph import Graphs
from nn_modules.code_names import INT_CODE, FLOAT_CODE, STR_CODE, BOOL_CODE

device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')


class BreakException(Exception):
    pass


def get_obj(hierarchy=None, widget_name='', condition=None):
    for w in hierarchy.walk_reverse(loopback=True):
        if widget_name.lower() == str(w).split(' ')[0].split('.')[-1].lower():
            if not condition:
                return w

            else:
                for key in condition.keys():
                    if key in dir(w) and getattr(w, key) == condition[key]:
                        return w


def map_properties(fn):
    from functools import wraps
    @wraps(fn)
    def _map_properties(*args, **kwargs):
        obj = args[0]
        algorithm = fn(obj)
        new_properties = {}

        for key in obj.properties.keys():
            # print(_property)
            property_type = obj.properties[key][0]
            value = obj.properties[key][1]

            if property_type == INT_CODE:
                new_properties.update({key: int(value)})

            elif property_type == BOOL_CODE:
                new_properties.update({key: [True if value == 'True' else False][0]})

            elif property_type == FLOAT_CODE:
                new_properties.update({key: float(value)})

            elif property_type == STR_CODE:
                new_properties.update({key: str(value)})

        # print(new_properties, obj)
        return algorithm(**new_properties)

    return _map_properties


def breaker(obj):
    if obj.end_task:
        raise BreakException


def checkpoint(fn):
    @wraps(fn)
    def _checkpoint(*args, **kwargs):
        self = args[0]
        properties = args[1]

        try:
            fn(self, properties)

        except BreakException:
            if self.save_checkpoint:
                name = self.model_name.replace(' ', '_').lower()
                torch.save(properties['model'].state_dict(),
                           f'checkpoints/{name}.state')
            properties['interface'].is_trained = False
            self.end_task = False
            return 0
    return _checkpoint


def record_graph(fn):
    @wraps(fn)
    def _record_graph(*args, **kwargs):
        interface = args[1]['interface']
        self = args[0]
        properties = args[1]

        # model_graph_view = get_obj(interface, 'ModelGraphView')
        # model_graph_view.current = 'graph'
        # print(interface)
        screen_manager = get_obj(interface, '_Container').request_obj('Manager')
        graph_tab_manager = screen_manager.get_screen('graph').children[-1].children[-1]

        losses, epochs = fn(self, properties)
        graph_tab_manager.add_tab(func_name=interface.model_name,
                                  _fkwargs={'graphs': {
                                      'Train / Loss': {
                                          'xlabel': 'Epochs',
                                          'ylabel': 'Loss',
                                          'losses': losses,
                                          'epochs': epochs
                                      }
                                  }})
        return 1

        # graph_tab_manager = get_obj(interface, 'ModelGraphView')
        # print(get_obj(interface, 'ModelGraphView'))
        # graph_tab_manager.add_tab(func_name=interface.model_name,
        #                           _fkwargs={'xmax': n_iter,
        #                                     'ymax': int(max(losses)) + 1})

    return _record_graph

# class LinksManager():
# 	def __init__(self):
# 		self.objs_list = {}

# 	def register_obj(self, name, obj):
# 		self.objs_list.update({name: obj})

# 	def remove_obj(self, name):
# 		self.objs_list.remove(name)

# 	def get_obj(self, name):
# 		return self.objs_list[name]
