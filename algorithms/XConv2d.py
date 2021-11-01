from torch.nn import Conv2d, BatchNorm2d, ReLU, MaxPool2d, Sequential


# class xconv2d:
#     def __init__(self):
#         super(xconv2d, self).__init__()
#         self.properties = None
#
#     def algorithm(self):
#         n_in = self.properties['n_in'][1]
#         n_out = self.properties['n_out'][1]
#         f_size = self.properties['f_size'][1]
#         stride = self.properties['stride'][1]
#         padding = self.properties['padding'][1]
#         b_norm = self.properties['b_norm'][1]
#         mpk_size = self.properties['mpk_size'][1]
#         mp_stride = self.properties['mp_stride'][1]
#
#         return Sequential(
#             Conv2d(in_channels=n_in,
#                    out_channels=n_out,
#                    kernel_size=f_size,
#                    stride=stride,
#                    padding=padding),
#             BatchNorm2d(b_norm),
#             ReLU(),
#             MaxPool2d(kernel_size=mpk_size,
#                       stride=mp_stride)
#         )

def algorithm(self):
    n_in = self.properties['n_in'][1]
    n_out = self.properties['n_out'][1]
    f_size = self.properties['f_size'][1]
    stride = self.properties['stride'][1]
    padding = self.properties['padding'][1]
    b_norm = self.properties['b_norm'][1]
    mpk_size = self.properties['mpk_size'][1]
    mp_stride = self.properties['mp_stride'][1]

    return Sequential(
        Conv2d(in_channels=n_in,
               out_channels=n_out,
               kernel_size=f_size,
               stride=stride,
               padding=padding),
        BatchNorm2d(b_norm),
        ReLU(),
        MaxPool2d(kernel_size=mpk_size,
                  stride=mp_stride)
    )
