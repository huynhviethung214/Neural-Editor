import math

import torch

from functools import wraps
from threading import Thread

from kivy.graphics import Bezier

from nn_modules.code_names import INT_CODE, FLOAT_CODE, STR_CODE, BOOL_CODE

device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')


class BreakException(Exception):
    pass


class CustomBezier(Bezier):
    def __init__(self, **kwargs):
        super(CustomBezier, self).__init__(**kwargs)
        self.begin = None
        self.end = None


class TerminalColor:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


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


def remove_node_from_interface(interface, node_name):
    for node in interface.nodes():
        if node.name == node_name:
            for node_gate in node.node_links():
                if node_gate.gate_type == 1:
                    interface.set_unbind(node_gate)
                else:
                    interface.set_unbind(node_gate.target)

            interface.remove_node(node)
            break


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


def combination(k, n):
    return math.factorial(n) / (math.factorial(k) *
                                math.factorial(n - 2))


# Formatting relationships according to the `node_links`
def formatting_rels(rels, node_links):
    formatted_rels = []
    current_rel = []

    for rel in rels:
        for rel_name in rel:
            for node_link in node_links:
                if f'{node_link.node.name} {node_link.name}' == rel_name:
                    current_rel.append(node_link)

                if len(current_rel) == 2:
                    formatted_rels.append(current_rel)
                    current_rel = []

    return formatted_rels


# Draw beziers from the formatted relationships to the interface
def draw_beziers(datas, interface):
    # print(f'Datas: {datas}')
    rels = formatting_rels(datas['rels'], interface.node_links())

    for coord, rel in zip(datas['beziers_coord'], rels):
        # Touch Down
        rel[0].c_pos = coord[0]

        # Touch Up
        rel[1].c_pos = coord[1]
        rel[1].target = rel[0]
        rel[1].t_pos = rel[0].c_pos

        rel[0].t_pos = coord[0]
        rel[0].target = rel[1]

        nl_index = rel[0].index()
        node_name = rel[0].node.name

        rel[0].target.node.connected_nodes.append(
            f'{node_name} {nl_index}'
        )

        rel[0].connected = 1
        rel[1].connected = 1

        # Draw Bezier
        bezier = interface.draw(*coord)
        bezier.begin = rel[0]
        bezier.end = rel[1]

        # print(bezier.begin.node.name, bezier.end.node.name)

        interface.links.append([rel[1], rel[0], bezier])
        interface.instructions.append(bezier)

    interface.template['beziers_coord'] = datas['beziers_coord']
    interface.rels = datas['rels']
