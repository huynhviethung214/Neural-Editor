import torch
from torch.optim import Adadelta
from utility.func_template import Template

built_in_args_list = {
    'Adadelta': {
        'params': [],
        'lr': 1.0,
        'rho': 0.9,
        'eps': 1e-06,
        'weight_decay': 0
    },
    'Adagrad': {
        'params': [],
        'lr': 0.01,
        'lr_decay': 0,
        'weight_decay': 0,
        'initial_accumulator_value': 0,
        'eps': 1e-10
    },
    'Adam': {
        'params': [],
        'lr': 0.001,
        'betas': (0.9, 0.999),
        'eps': 1e-08,
        'weight_decay': 0,
        'amsgrad': False
    },
    'AdamW': {
        'params': [],
        'lr': 0.001,
        'betas': (0.9, 0.999),
        'eps': 1e-08,
        'weight_decay': 0.01,
        'amsgrad': False
    },
    'SparseAdam': {
        'params': [],
        'lr': 0.001,
        'betas': (0.9, 0.999),
        'eps': 1e-08
    },
    'Adamax': {
        'params': [],
        'lr': 0.002,
        'betas': (0.9, 0.999),
        'eps': 1e-08,
        'weight_decay': 0
    },
    'ASGD': {
        'params': [],
        'lr': 0.01,
        'lambd': 0.0001,
        'alpha': 0.75,
        't0': 1000000.0,
        'weight_decay': 0
    },
    'LBFGS': {
        'params': [],
        'lr': 1,
        'max_iter': 20,
        'max_eval': 20 * 1.25,
        'tolerance_grad': 1e-07,
        'tolerance_change': 1e-09,
        'history_size': 100,
        'line_search_fn': ''
    },
    'RMSprop': {
        'params': [],
        'lr': 0.01,
        'alpha': 0.99,
        'eps': 1e-08,
        'weight_decay': 0,
        'momentum': 0,
        'centered': False
    },
    'Rprop': {
        'params': [],
        'lr': 0.01,
        'etas': (0.5, 1.2),
        'step_sizes': (1e-06, 50)
    },
    'SGD': {
        'params': [],
        'lr': 0.01,
        'momentum': 0,
        'dampening': 0,
        'weight_decay': 0,
        'nesterov': False
    }
}

built_in_source = torch.optim


# f_list = {}
# fname_list = []


def generate_funcs():
    for f in dir(built_in_source):
        if '__' not in f and f[0].isupper() and f in built_in_args_list.keys():
            try:
                src_name = str(built_in_source).split(' ')[1]
                src_name = src_name.split("'")[1]

                module = __import__(src_name, fromlist=[f])
                _func = getattr(module, f)
                fname = '___{0}'.format(f)

                globals()[fname] = type(fname, (Template,),
                                        {
                                            'prop_dict': built_in_args_list[f]
                                            # '__init__': __init__
                                        })
                globals()[fname] = globals()[fname](name=f, alg=_func)
            # func = Template(name=f, alg=_func)
            # func.prop_dict = built_in_args_list[f]

            # fname_list.append(f)
            # f_list.update({f: func})
            # print(fname)
            except Exception:
                pass


# if __name__ == '__main__':
# 	generate_funcs()

generate_funcs()
# print(type(globals()[fname_list[0]]))
# print(globals()[fname].algorithm())

# custom_source = custom_optimizer


# class ___Adadelta():
# 	prop_dict = {
# 		'params': [],
# 		'lr': 1.0,
# 		'rho': 0.9,
# 		'eps': 1e-06,
# 		'weight_decay': 0
# 	}

# 	def __init__(self):
# 		super(___Adadelta, self).__init__()

# 	def algorithm(self):
# 		return Adadelta(
# 			params = self.prop_list['params'],
# 			lr = self.prop_list['lr'],
# 			rho = self.prop_list['rho'],
# 			eps = self.prop_list['eps'],
# 			weight_decay = self.prop_list['weight_decay']
# 		)

# 	def __str__(self):
# 		return 'Adadelta'
