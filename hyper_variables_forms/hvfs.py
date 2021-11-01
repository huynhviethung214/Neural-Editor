import nn_criterions.criterions
import nn_optims.optims
import datasets_processors.generate_processors
import nn_algorithms.generate_training_algorithms
import nn_algorithms.generate_evaluating_algorithms

from utility.base_form.baseform import BaseForm


class DatasetForm(BaseForm):
    def __init__(self, **kwargs):
        super(DatasetForm, self).__init__()
        self.add_drop_down_list(source=datasets_processors.generate_processors)
        BaseForm._children.append(self)


class CriterionForm(BaseForm):
    def __init__(self, **kwargs):
        super(CriterionForm, self).__init__()
        self.add_drop_down_list(source=nn_criterions.criterions)
        BaseForm._children.append(self)


class OptimizerForm(BaseForm):
    def __init__(self, **kwargs):
        super(OptimizerForm, self).__init__()
        self.add_drop_down_list(source=nn_optims.optims)
        BaseForm._children.append(self)


class TrainingForm(BaseForm):
    def __init__(self, **kwargs):
        super(TrainingForm, self).__init__()
        self.add_drop_down_list(source=nn_algorithms.generate_training_algorithms)
        BaseForm._children.append(self)
        

class EvaluatingForm(BaseForm):
    def __init__(self, **kwargs):
        super(EvaluatingForm, self).__init__()
        self.add_drop_down_list(source=nn_algorithms.generate_evaluating_algorithms)
        BaseForm._children.append(self)
