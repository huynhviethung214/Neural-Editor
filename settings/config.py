import json
import GPUtil
from os.path import exists
from collections import UserDict
from cpuinfo import get_cpu_info

import torch


class Configuration(dict):
    def __init__(self):
        super(Configuration, self).__init__()

        self.fpath = 'settings/settings.json'
        self.devices = self.get_devices_info()
        self.default_config = {}

        self.reload_config()

    def __setitem__(self, key, value):
        super().__setitem__(key, value)

    def __getitem__(self, item):
        if item == 'device':
            return self.default_config[item]
        return self.get(item)

    def reload_config(self):
        if exists(self.fpath):
            with open(self.fpath, 'r') as f:
                configs = json.load(f)

                for key in configs.keys():
                    # print(key)
                    self.update({key: configs[key]})
                self.default_config = configs
        else:
            with open(self.fpath, 'w') as f:
                json.dump(self.default_config,
                          f,
                          sort_keys=True,
                          indent=4)

    @staticmethod
    def get_devices_info():
        devices_info = []

        for gpu in GPUtil.getGPUs():
            devices_info.append(f'{gpu.name} (cuda:{gpu.id})')

        cpu_info = get_cpu_info()['brand_raw']
        devices_info.append(f'{cpu_info} (cpu)')

        return tuple(devices_info)


configs = Configuration()
# print(configs.keys())
