import torch

from functools import wraps
from threading import Thread

from nn_modules.code_names import INT_CODE, FLOAT_CODE, STR_CODE, BOOL_CODE

device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')


class BreakException(Exception):
    pass


# Dynamically retrieve a widget from it's hierarchy
def get_obj(hierarchy=None, widget_name='', condition=None):
    for w in hierarchy.walk_reverse(loopback=True):
        if widget_name.lower() == str(w).split(' ')[0].split('.')[-1].lower():
            # If there aren't any condition then return widget `w`
            if not condition:
                return w
            # Else then the widget's variables must satisfied the given condition
            else:
                for key in condition.keys():
                    # Compare the variables of widget `w` in the hierarchy
                    # with custom condition (Ex: {'name': 'Linear 1'})
                    if key in dir(w) and getattr(w, key) == condition[key]:
                        return w


def update_progress_bar(obj, epoch, epochs):
    obj.progress_bar.max = epochs
    obj.progress_bar.value = epoch
    obj.progress_indicator.text = f'{int(obj.progress_bar.value_normalized * 100)}% / 100%'


def breaker(obj):
    if obj.end_task:
        raise BreakException


def map_properties(fn):
    @wraps(fn)
    def _map_properties(*args, **kwargs):
        obj = args[0]
        algorithm = fn(obj)
        new_properties = {}

        for key in obj.properties.keys():
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

        return algorithm(**new_properties)

    return _map_properties


def checkpoint(fn):
    @wraps(fn)
    def _checkpoint(*args, **kwargs):
        self = args[0]
        properties = args[1]

        try:
            fn(self, properties)
            return 1

        except BreakException:
            if self.save_checkpoint:
                name = self.model_name.replace(' ', '_').lower()
                torch.save(properties['model'].state_dict(),
                           f'checkpoints/{name}.state')
            properties['interface'].is_trained = False
            self.end_task = False
            return 1

    return _checkpoint


# For now it can only plot loss / epoch
def record_graph(fn):
    @wraps(fn)
    def _record_graph(*args, **kwargs):
        interface = args[1]['interface']
        self = args[0]
        properties = args[1]

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

    return _record_graph
