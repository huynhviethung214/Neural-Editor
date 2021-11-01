from torch import Tensor


class L1Loss:
    _properties = {}

    def __init__(self):
        L1Loss._properties.update({'size_average': [bool, None]})
        L1Loss._properties.update({'reduce': [bool, None]})
        L1Loss._properties.update({'reduction': [str, 'mean']})


class MSELoss:
    _properties = {}

    def __init__(self):
        MSELoss._properties.update({'size_average': [bool, True]})
        MSELoss._properties.update({'reduce': [bool, True]})
        MSELoss._properties.update({'reduction': [str, 'mean']})


class CrossEntropyLoss:
    _properties = {}

    def __init__(self):
        CrossEntropyLoss._properties.update({'weight': [Tensor, None]})
        CrossEntropyLoss._properties.update({'size_average': [bool, None]})
        CrossEntropyLoss._properties.update({'ignore_index': [int, None]})
        CrossEntropyLoss._properties.update({'reduce': [bool, True]})
        CrossEntropyLoss._properties.update({'reduction': [str, 'mean']})


class CTCLoss:
    _properties = {}

    def __init__(self):
        CTCLoss._properties.update({'blank': [int, None]})
        CTCLoss._properties.update({'reduction': [str, 'mean']})
        CTCLoss._properties.update({'zero_infinity': [bool, False]})


class NLLLoss:
    _properties = {}

    def __init__(self):
        NLLLoss._properties.update({'weight': [Tensor, None]})
        NLLLoss._properties.update({'size_average': [bool, None]})
        NLLLoss._properties.update({'ignore_index': [int, -100]})
        NLLLoss._properties.update({'reduce': [bool, True]})
        NLLLoss._properties.update({'reduction': [str, 'mean']})


class PoissonNLLLoss:
    _properties = {}

    def __init__(self):
        PoissonNLLLoss._properties.update({'log_input': [bool, True]})
        PoissonNLLLoss._properties.update({'full': [bool, False]})
        PoissonNLLLoss._properties.update({'size_average': [bool, True]})
        PoissonNLLLoss._properties.update({'eps': [float, 1e-08]})
        PoissonNLLLoss._properties.update({'reduce': [bool, True]})
        PoissonNLLLoss._properties.update({'reduction': [str, 'mean']})


class KLDivLoss:
    _properties = {}

    def __init__(self):
        KLDivLoss._properties.update({'size_average': [bool, True]})
        KLDivLoss._properties.update({'reduce': [bool, True]})
        KLDivLoss._properties.update({'reduction': [str, 'mean']})


class BCELoss:
    _properties = {}

    def __init__(self):
        BCELoss._properties.update({'weight': [Tensor, None]})
        BCELoss._properties.update({'size_average': [bool, True]})
        BCELoss._properties.update({'reduce': [bool, True]})
        BCELoss._properties.update({'reduction': [str, 'mean']})


class BCEWithLogitsLoss:
    _properties = {}

    def __init__(self):
        BCEWithLogitsLoss._properties.update({'weight': [Tensor, None]})
        BCEWithLogitsLoss._properties.update({'size_average': [bool, True]})
        BCEWithLogitsLoss._properties.update({'reduce': [bool, True]})
        BCEWithLogitsLoss._properties.update({'reduction': [str, 'mean']})
        BCEWithLogitsLoss._properties.update({'pos_weight': [Tensor, None]})


class MarginRankingLoss:
    _properties = {}

    def __init__(self):
        MarginRankingLoss._properties.update({'margin': [float, 0.0]})
        MarginRankingLoss._properties.update({'size_average': [bool, True]})
        MarginRankingLoss._properties.update({'reduce': [bool, True]})
        MarginRankingLoss._properties.update({'reduction': [str, 'mean']})


class HingeEmbeddingLoss:
    _properties = {}

    def __init__(self):
        HingeEmbeddingLoss._properties.update({'margin': [float, 1.0]})
        HingeEmbeddingLoss._properties.update({'size_average': [bool, True]})
        HingeEmbeddingLoss._properties.update({'reduce': [bool, True]})
        HingeEmbeddingLoss._properties.update({'reduction': [str, 'mean']})


class MultiLabelMarginLoss:
    _properties = {}

    def __init__(self):
        MultiLabelMarginLoss._properties.update({'size_average': [bool, True]})
        MultiLabelMarginLoss._properties.update({'reduce': [bool, True]})
        MultiLabelMarginLoss._properties.update({'reduction': [str, 'mean']})


class CosineEmbeddingLoss:
    _properties = {}

    def __init__(self):
        CosineEmbeddingLoss._properties.update({'margin': [float, 0.0]})
        CosineEmbeddingLoss._properties.update({'size_average': [bool, True]})
        CosineEmbeddingLoss._properties.update({'reduce': [bool, True]})
        CosineEmbeddingLoss._properties.update({'reduction': [str, 'mean']})


class MultiMarginLoss:
    _properties = {}

    def __init__(self):
        MultiMarginLoss._properties.update({'p': [int, 1]})
        MultiMarginLoss._properties.update({'margin': [float, 1.0]})
        MultiMarginLoss._properties.update({'weight': [Tensor, None]})
        MultiMarginLoss._properties.update({'size_average': [bool, True]})
        MultiMarginLoss._properties.update({'reduce': [bool, True]})
        MultiMarginLoss._properties.update({'reduction': [str, 'mean']})


class MultiMarginLoss:
    _properties = {}

    def __init__(self):
        MultiMarginLoss._properties.update({'margin': [float, 1.0]})
        MultiMarginLoss._properties.update({'p': [int, 2]})
        MultiMarginLoss._properties.update({'eps': [float, 1e-06]})
        MultiMarginLoss._properties.update({'swap': [bool, False]})
        MultiMarginLoss._properties.update({'size_average': [bool, True]})
        MultiMarginLoss._properties.update({'reduce': [bool, True]})
        MultiMarginLoss._properties.update({'reduction': [str, 'mean']})


class AdaptiveLogSoftmaxWithLoss:
    _properties = {}

    def __init__(self):
        AdaptiveLogSoftmaxWithLoss._properties.update({'in_features': [int, None]})
        AdaptiveLogSoftmaxWithLoss._properties.update({'n_classes': [int, None]})
        AdaptiveLogSoftmaxWithLoss._properties.update({'cutoffs': [list, 1e-06]})
        AdaptiveLogSoftmaxWithLoss._properties.update({'div_value': [int, None]})
        AdaptiveLogSoftmaxWithLoss._properties.update({'head_bias': [bool, True]})


class MultiLabelSoftMarginLoss:
    _properties = {}

    def __init__(self):
        MultiLabelSoftMarginLoss._properties.update({'weight': [Tensor, None]})
        MultiLabelSoftMarginLoss._properties.update({'size_average': [bool, True]})
        MultiLabelSoftMarginLoss._properties.update({'reduce': [bool, True]})
        MultiLabelSoftMarginLoss._properties.update({'reduction': [str, 'mean']})
