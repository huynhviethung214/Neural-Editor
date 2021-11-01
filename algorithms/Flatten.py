import torch
from torch.nn import Module

from nn_modules.node import CustomValueInput


# class flatten:
#     # properties = None
#
#     def __init__(self):
#         super(flatten, self).__init__()
#         self.properties = None
#         # self.flattened = 0
#
#     #     self.next_node = self.properties['obj'][1].output_node.target
#     #     self.properties['obj'][1].output_node.state_event.bind(on_state=self.set_target_value)
#     #
#     # def set_target_value(self, state):
#     #     for widget in self.next_node.sub_layout.children:
#     #         if type(widget) == CustomValueInput and 'out' in widget.name:
#     #             print(widget.text)
#     #             widget.text = str(self.flattened)
#
#     def algorithm(self):
#         return _flatten()


class _flatten(Module):
    def forward(self, x):
        # print(x.size(0))
        try:
            # print(x)
            # return x.view(x.size(0), -1)
            return torch.flatten(x, start_dim=0)
            # return torch.reshape(x, (x.size(0),))
        except RuntimeError:
            pass



def algorithm(self):
    return _flatten()
