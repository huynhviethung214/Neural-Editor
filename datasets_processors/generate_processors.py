# built_in_args_list = {
# 	'ImageProcessor': {
# 		'fpath': 'D:\\Python Projects\\Project Alpha\\S&U\\PyTorch\\TreeRecognition\\test_set',
# 		# 'split': 0.3,
# 		'shuffle': True,
# 		'width': 300,
# 		'height': 300,
# 		'channels': 3,
# 		'output_file': 'tree_dataset'
# 	},
# 	'BinaryProcessor': {
# 		'fpath': 'test_set\\binary_dataset.txt'
# 	}
# }

# source = nn_processors.processors
#
#
# def generate_funcs():
# 	for f in dir(source):
# 		for key in built_in_args_list.keys():
# 			try:
# 				if f == key:
# 					src_name = str(source).split(' ')[1]
# 					src_name = src_name.split("'")[1]
#
# 					module = __import__(src_name, fromlist=[f])
# 					_func = getattr(module, f)
# 					fname = '___{0}'.format(f)
#
# 					globals()[fname] = type(fname, (Template,),
# 											{
# 												'prop_dict': built_in_args_list[f]
# 												# '__init__': __init__
# 											})
# 					globals()[fname] = globals()[fname](name=f, alg=_func)
# 					break
#
# 			except Exception as e:
# 				raise e

import os

from utility.func_template import Template

fpath = 'nn_processors\\processors'


for f in os.listdir(fpath):
	if '_' not in f:
		func_name = f.split('.')[0]
		source = fpath.replace('\\', '.')

		module = __import__(source + f'.{func_name}', fromlist=[func_name, 'kwargs'])
		processor = getattr(module, f.split('.')[0])
		args = getattr(module, 'kwargs')
		new_func_name = f'___{func_name}'

		globals()[new_func_name] = type(new_func_name, (Template,), {'prop_dict': args[func_name]})
		globals()[new_func_name] = globals()[new_func_name](name=func_name, alg=processor)


# generate_funcs()
