import logging
from time import sleep

import torch
import queue
import numpy
import gc

from queue import Queue
from threading import Thread, Lock
from multiprocessing import JoinableQueue, Process

from utility.utils import get_obj
from utility.base_form.baseform import BaseForm
from settings.config import configs
from message_box.message_box import MessageBox


class TrainingManager:
    def __init__(self, **kwargs):
        super(TrainingManager, self).__init__(**kwargs)
        self.end_task = False
        self.save_checkpoint = True
        self.training = False
        self.terminate_threads = False

        self.jobs = Queue()
        self._jobs = []

        self.queue_job_thread = Thread(target=self._queue_job, daemon=True)
        self.queue_job_thread.start()

        self.progress_bar = None
        self.progress_indicator = None

    def setup_train(self, model=None, obj=None, interface=None):
        # print('Add Job')
        train_properties, train_code = BaseForm._children[3].get_alg(_type=2)
        eval_properties, eval_code = BaseForm._children[4].get_alg(_type=3)

        code = {'training': train_code,
                'evaluating': eval_code}

        properties = {'training': train_properties,
                      'evaluating': eval_properties}

        criterion, optimizer, dataset = self.get_functions(model=model)

        if not self.progress_bar:
            self.progress_bar = get_obj(interface, 'ProgressBar')
            self.progress_indicator = get_obj(interface, 'ProgressIndicator')

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

        self._jobs.append([properties, code, obj])

        # Dynamic threading for training
        # self.setup_train(model, properties, code, obj, interface)

    @staticmethod
    def get_functions(model=None):
        try:
            criterion = BaseForm._children[0].get_alg()
            optimizer = BaseForm._children[1].get_alg(params=model.parameters())
            dataset = BaseForm._children[2].get_alg(_type=1)

            return criterion, optimizer, dataset

        except Exception as e:
            raise e

    def _queue_job(self):
        while not self.terminate_threads:
            sleep(1)

            if self.terminate_threads:
                break

            if len(self._jobs) > 0:
                job = self._jobs[0]
                self._jobs.pop(0)
                self.jobs.put(job)

                self._queue_training()

                self.jobs.join()

    # TODO: FREE MEMORY AFTER BREAKING TRAINING/EVALUATING PROCESS
    def _queue_training(self):
        properties, code, obj = self.jobs.get()

        interface = properties['training']['interface']
        model_name = get_obj(interface, 'TrainedModelLabel')
        progress_indicator = get_obj(interface, 'ProgressIndicator')

        # Reset Progress Bar to 0
        self.progress_bar.value = 0

        # Set Model's name
        model_name.text = f'Model: {interface.model_name}'

        # Reset ProgressIndicator text
        progress_indicator.text = f'0%/100%'

        ret = self._train(properties, code)

        if ret:
            obj.text = '>'
            obj.is_training = False

            torch.cuda.empty_cache()
            training_properties = properties['training']

            if 'interface' in training_properties.keys():
                if training_properties['interface'].is_trained:
                    # MessageBox(message_type='Training Succeed',
                    #            message='').open()
                    pass
            # print('Close Job')
            self.jobs.task_done()

        gc.collect()

    # Dynamic evaluating algorithm
    def _evaluate(self, properties=None, code=None):
        try:
            exec(code, locals())
            locals()['evaluating_alg'](self, properties)

        except Exception as e:
            logging.warning(f'[EVALUATING]: {e}')
            # pass
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

        except Exception as e:
            logging.warning(f'TRAINING: {e}')
            raise e
            # pass
            # MessageBox(message=str(e),
            #            message_type='Error Message').open()
            # return 0

        return 1

    # def _update(self, val, _type):
    #     self.progress_bar.value = int(floor(val))
    #     self.progress_bar.parent.children[0].text = f'[{_type}]:[{int(self.progress_bar.value)}%/100%]'
