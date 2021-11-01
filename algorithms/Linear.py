from torch.nn import Linear


# class linear:
#     # properties = None
#
#     def __init__(self):
#         super(linear, self).__init__()
#         self.properties = None
#
#     def algorithm(self):
#         return Linear(self.properties['n_in'][1],
#                       self.properties['n_out'][1],
#                       self.properties['bias'][1])

def algorithm(self):
    return Linear(self.properties['n_in'][1],
                  self.properties['n_out'][1],
                  self.properties['bias'][1])
