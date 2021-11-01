from torch.nn import Conv2d


# class conv2d:
#     def __init__(self):
#         self.properties = None
#
#     def algorithm(self):
#         return Conv2d(self.properties['in_channels'],
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
    return Conv2d(self.properties['in_channels'][1],
                  self.properties['out_channels'][1],
                  self.properties['kernel_size'][1],
                  self.properties['stride'][1],
                  self.properties['padding'][1],
                  self.properties['dilation'][1],
                  self.properties['groups'][1],
                  self.properties['bias'][1],
                  self.properties['padding_mode'][1]
                  )
