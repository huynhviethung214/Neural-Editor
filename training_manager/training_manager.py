import torch
import queue
import numpy
import gc

from torch.autograd import Variable

from threading import Thread
from multiprocessing import Process
from math import floor
from queue import Queue

from utility.utils import get_obj
from utility.base_form.baseform import BaseForm
from settings.config import configs
from message_box.message_box import MessageBox


class TrainingManager:
    def __init__(self, **kwargs):
        super(TrainingManager, self).__init__(**kwargs)
        self.std_val = 0
        self.end_task = False
        self.save_checkpoint = True
        self.model_name = None
        self.queue = Queue(4)

        self.thread = Thread(target=self._queue_training, daemon=True)
        self.thread.start()

    # def kill_process(self):
    #     try:
    #         self._break = True
    #         self.thread.join()
    #         self.thread.is_alive()
    #
    #     except AttributeError as e:
    #         pass

    def add_job(self, model=None, obj=None, interface=None):
        # print('Add Job')
        train_properties, train_code = BaseForm._children[3].get_alg(_type=2)
        eval_properties, eval_code = BaseForm._children[4].get_alg(_type=3)

        code = {'training': train_code,
                'evaluating': eval_code}

        properties = {'training': train_properties,
                      'evaluating': eval_properties}

        # Dynamic threading for training
        self.setup_train(model, properties, code, obj, interface)

    @staticmethod
    def get_functions(model=None):
        try:
            criterion = BaseForm._children[0].get_alg()
            optimizer = BaseForm._children[1].get_alg(params=model.parameters())
            dataset = BaseForm._children[2].get_alg(_type=1)

            return criterion, optimizer, dataset

        except Exception as e:
            raise e

    def setup_train(self, model, properties, code, obj, interface):
        criterion, optimizer, dataset = self.get_functions(model=model)

        properties['evaluating'].update({'obj': self,
                                         'eval_code': code['evaluating'],
                                         'model': model,
                                         'device': configs['device']['id'],
                                         'dataset': dataset,
                                         'interface': interface})

        properties['training'].update({'criterion': criterion,
                                       'optimizer': optimizer,
                                       'dataset': dataset,
                                       'obj': self,
                                       'model': model,
                                       'device': configs['device']['id'],
                                       'weight_path': configs['weight_path'],
                                       'eval_properties': properties['evaluating'],
                                       'interface': interface})

        self.queue.put([properties, code, obj])

    # TODO: FREE MEMORY AFTER BREAKING TRAINING/EVALUATING PROCESS
    def _queue_training(self):
        while True:
            if self.queue.not_empty:
                properties, code, obj = self.queue.get()
                ret = self._train(properties, code)
                # print(ret)

                if ret:
                    obj.text = '>'
                    obj.is_training = False

                    torch.cuda.empty_cache()
                    training_properties = properties['training']

                    if 'interface' in training_properties.keys():
                        if training_properties['interface'].is_trained:
                            MessageBox(message_type='Training Succeed',
                                       message='').open()
                    # print('Close Job')

                # print(gc.get_count())
                # gc.collect()
                # print(gc.get_count())
                self.queue.task_done()

    # Dynamic evaluating algorithm
    def _evaluate(self, properties=None, code=None):
        try:
            exec(code, locals())
            locals()['evaluating_alg'](self, properties)

            return 1

        except Exception as e:
            raise e
            # MessageBox(message=str(e),
            #            message_type='Error Message').open()
            #
            # return 0

    # COULD MERGE TRAINING AND EVALUATING FUNCTIONS INTO 1 FUNCTION
    # Dynamic training algorithm
    def _train(self, properties=None, code=None):
        try:
            exec(code['training'], locals())
            locals()['training_alg'](self, properties['training'])

            return 1

        except Exception as e:
            raise e
            # MessageBox(message=str(e),
            #            message_type='Error Message').open()
            # return 0

    # def _update(self, val, _type):
    #     self.progress_bar.value = int(floor(val))
    #     self.progress_bar.parent.children[0].text = f'[{_type}]:[{int(self.progress_bar.value)}%/100%]'
