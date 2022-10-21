import math
from json import JSONEncoder

import torch
from functools import wraps

from kivy.clock import Clock
from kivy.graphics import Bezier, Line
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.widget import Widget

from nn_modules.code_names import *

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


def get_bezier_endpoints(bezier):
    points = bezier.points
    beziers_coord = [
        [points[0], points[1]],
        [points[-2], points[-1]]
    ]

    return beziers_coord


def round_pos(pos, precision=1):
    return [round(pos[0], precision), round(pos[1], precision)]


def remove_node_from_interface(interface, ref_node_name):
    for node_name in interface.nodes.keys():
        if node_name == ref_node_name:
            node = interface.nodes[node_name]

            for node_gate in node.node_links():
                # gate_type = gate_type.schema_get('gate_type')
                node_gate.unbind()
                # if node_gate == 1:
                #     interface.set_unbind(node_gate)
                # else:
                #     interface.set_unbind(node_gate.target)

            interface.remove_node(node)
            break


def update_progress_bar(obj, epoch, epochs):
    obj.progress_bar.max = epochs
    obj.progress_bar.value = epoch
    obj.progress_indicator.text = f'{int(obj.progress_bar.value_normalized * 100)}% / 100%'


def breaker(obj):
    if obj.end_task:
        raise BreakException


# def get_algorithm(node_class):
#     module = __import__(f'algorithms.{node_class}',
#                         fromlist=['algorithm'])
#     algo = getattr(module, 'algorithm')
#
#     return algo


def map_properties(fn):
    @wraps(fn)
    def _map_properties(*args, **kwargs):
        obj = args[0]  # Node object
        algorithm = fn(obj)  # Passing in `self` as argument
        new_properties = {}
        node_properties = obj.schema['properties']

        for key in node_properties.keys():
            property_type = node_properties[key][0]
            value = node_properties[key][1]

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

        except BreakException:
            properties['interface'].is_trained = False
            self.end_task = False

        if self.save_checkpoint:
            name = self.model_name.replace(' ', '_').lower()
            torch.save(properties['model'].state_dict(),
                       properties['weight_path'] + f'/{name}.w')
            torch.cuda.empty_cache()
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
        # graph_tab_manager = screen_manager.get_screen('graph').children[-1].children[-1]

        losses, epochs = fn(self, properties)
        # graph_tab_manager.add_tab(func_name=interface.model_name,
        #                           _fkwargs={'graphs': {
        #                               'Train / Loss': {
        #                                   'xlabel': 'Epochs',
        #                                   'ylabel': 'Loss',
        #                                   'losses': losses,
        #                                   'epochs': epochs
        #                               }
        #                           }})

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
            for node_link_name in node_links.keys():
                node_link = node_links[node_link_name]
                node = node_link.node

                if f'{node.name} {node_link.name}' == rel_name:
                    current_rel.append(node_link)

                if len(current_rel) == 2:
                    formatted_rels.append(current_rel)
                    current_rel = []

    return formatted_rels


# Draw beziers from the formatted relationships to the interface
def draw_beziers(schema, interface):
    rels = formatting_rels(schema['cmap'], interface.node_links)

    for coord, rel in zip(schema['beziers_coord'], rels):
        # Touch Down
        rel[0].schema_set('c_pos', coord[0])
        rel[0].schema_set('target_pos', coord[1])
        rel[0].schema_set('target', f'{rel[1].node.name} {rel[1].name}')

        # Touch Up
        rel[1].schema_set('c_pos', coord[1])
        rel[1].schema_set('target_pos', coord[0])
        rel[1].schema_set('target', f'{rel[0].node.name} {rel[0].name}')

        rel[0].schema_set('connected', True)
        rel[1].schema_set('connected', True)

        # Draw Bezier
        bezier = interface.draw(*coord)
        bezier.begin = rel[0]
        bezier.end = rel[1]

        interface.instructions.append(bezier)
