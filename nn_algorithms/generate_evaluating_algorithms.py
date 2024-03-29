import utility.algorithms.base_algorithm
from utility.func_template import Template

kwargs = {
    'PerceptronExample': {
        'file_path': 'hyper_variables_forms\\perceptron_example\\eval\\evaluating.py',
        'epochs': 10
    }
}

source = utility.algorithms.base_algorithm
src_name = str(source).split(' ')[1]
src_name = src_name.split("'")[1]

module = __import__(src_name, fromlist=['BaseAlgorithm'])
_func = getattr(module, 'BaseAlgorithm')


for f in kwargs.keys():
    try:
        fname = '___{0}'.format(f)

        globals()[fname] = type(fname, (Template,),
                                {
                                    'prop_dict': kwargs[f]
                                })
        globals()[fname] = globals()[fname](name=f, alg=_func)

    except KeyError as e:
        raise e
