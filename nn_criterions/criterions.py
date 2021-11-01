# src_name = str(source).split(' ')[1]
# src_name = src_name.split("'")[1]

# module = __import__(src_name, fromlist=[func])
# _func = getattr(module, func)
# _func = _func.__new__(_func)

import torch
from utility.func_template import Template

# device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')

built_in_args_list = {
    'L1Loss': {
        'size_average': True,
        'reduce': True,
        'reduction': 'mean'
    },
    'MSELoss': {
        'size_average':True,
        'reduce':True,
        'reduction': 'mean'
    },
    'CrossEntropyLoss': {
        'weight': None,
        'size_average':True,
        'ignore_index': -100,
        'reduce':True,
        'reduction': 'mean'
    },
    'CTCLoss': {
        'blank': 0,
        'reduction': 'mean',
        'zero_infinity': False
    },
    'NLLLoss': {
        'weight': None,
        'size_average':True,
        'ignore_index': -100,
        'reduce':None,
        'reduction': 'mean'
    },
    'PoissonNLLLoss': {
        'log_input': True,
        'full': False,
        'size_average':True,
        'eps': 1e-08,
        'reduce':None,
        'reduction': 'mean'
    },
    'KLDivLoss': {
        'size_average':True,
        'reduce':True,
        'reduction': 'mean'
    },
    'BCELoss': {
        'weight': None,
        'size_average':True,
        'reduce':True,
        'reduction': 'mean'
    },
    'BCEWithLogitsLoss': {
        'weight': None,
        'size_average':True,
        'reduce':True,
        'reduction': 'mean',
        'pos_weight': None
    },
    'MarginRankingLoss': {
        'margin': 0.0,
        'size_average':True,
        'reduce':True,
        'reduction': 'mean'
    },
    'HingeEmbeddingLoss': {
        'margin': 1.0,
        'size_average':True,
        'reduce':True,
        'reduction': 'mean'
    },
    'SmoothL1Loss': {
        'size_average':True,
        'reduce':True,
        'reduction': 'mean'
    },
    'MultiLabelSoftMarginLoss': {
        'weight': None,
        'size_average':True,
        'reduce':True,
        'reduction': 'mean'
    },
    'CosineEmbeddingLoss': {
        'margin': 0.0,
        'size_average':True,
        'reduce':True,
        'reduction': 'mean'
    },
    'MultiMarginLoss': {
        'p': 1,
        'margin': 1.0,
        'weight': None,
        'size_average':True,
        'reduce':True,
        'reduction': 'mean'
    },
    'TripletMarginLoss': {
        'margin': 1.0,
        'p': 2.0,
        'eps': 1e-06,
        'swap': False,
        'size_average':True,
        'reduce':True,
        'reduction': 'mean'
    }
}

built_in_source = torch.nn


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
            except Exception:
                pass


generate_funcs()
