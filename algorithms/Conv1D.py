from torch.nn import Conv1d


#
#
# class conv1d:
#     def __init__(self):
#         self.properties = None
#
#     def algorithm(self):
#         return Conv1d(self.properties['in_channels'],
#                       self.properties['out_channels'],
#                       self.properties['kernel_size'],
#                       self.properties['stride'],
#                       self.properties['padding'],
#                       self.properties['dilation'],
#                       self.properties['groups'],
#                       self.properties['bias'],
#                       self.properties['padding_mode']
#                       )

def algorithm(self):
    return Conv1d(self.properties['in_channels'][1],
                  self.properties['out_channels'][1],
                  self.properties['kernel_size'][1],
                  self.properties['stride'][1],
                  self.properties['padding'][1],
                  self.properties['dilation'][1],
                  self.properties['groups'][1],
                  self.properties['bias'][1],
                  self.properties['padding_mode'][1]
                  )
