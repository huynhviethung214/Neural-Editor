import importlib
import json
import nn_modules

from kivy.uix.filechooser import FileChooserIconView

from nn_modules.code_names import STACKED, LAYER_CODE
from node_editor.node_editor import NodeEditor
from utility.rightclick_toolbar.rightclick_toolbar import RightClickMenu
from utility.utils import get_obj


class FileChooser(FileChooserIconView):
    def __init__(self, **kwargs):
        super(FileChooser, self).__init__()
        self.rootpath = 'models'
        self.selected = None
        self.touch = None

        self.obj = kwargs.get('obj')
        self.component_panel = kwargs.get('component_panel')

        self.bind(on_touch_up=self.open_menu)
        # self.bind(selection=lambda obj, value: setattr(self, 'selected', value))
        self.bind(selection=self.select)

    # ADD EXCEPTION HANDLER FOR NOT CHOOSING INPUT AND OUTPUT LAYER IN CURRENT SELECTED MODEL
    def model_to_stacked(self):
        properties = {}
        node_name = self.selected.split('.')[0]
        node_name = node_name[0].upper() + node_name[1:]
        nl_input = None
        nl_output = None

        with open('nn_modules/nn_nodes.json', 'r') as fn:
            nodes = json.load(fn)

            with open(f'models/{self.selected}', 'r') as fm:
                model_json = json.load(fm)
                model = model_json['model']

                for node in model.keys():
                    for property_key in model[node]['properties'].keys():
                        if property_key == 'Layer':
                            if model[node]['properties'][property_key][1] == 'Input Layer':
                                nl_input = {'nl_input': nodes[node.split(' ')[0]]['nl_input']}
                                nl_input['nl_input']['type'] = 'input'

                            elif model[node]['properties'][property_key][1] == 'Output Layer':
                                nl_output = {'nl_output': nodes[node.split(' ')[0]]['nl_output']}
                                nl_output['nl_output']['type'] = 'output'

                properties.update({'Layer': [LAYER_CODE, 'Hidden Layer']})
                properties.update({'node_type': STACKED})
                properties.update({'model': model})
                properties.update({'rels': model_json['rels']})
                properties.update({'beziers_coord': model_json['beziers_coord']})
                properties.update(nl_input)
                properties.update(nl_output)

            nodes.update({node_name: properties})
            code_template = self.get_code_template(node_name)
            self.add_alg_file(node_name, code_template)

            with open('nn_modules/nn_nodes.json', 'w') as f:
                json.dump(nodes, f, sort_keys=True, indent=4)

            importlib.reload(nn_modules.nn_components)
            self.component_panel.update_panel()

        return True

    @staticmethod
    def add_alg_file(node_name, code_template):
        with open('algorithms/{0}.py'.format(node_name), 'w') as f:
            f.write(code_template)

    @staticmethod
    def get_code_template(node_name):
        with open('i_modules/stacked_code_template.py', 'r') as f:
            lines = f.readlines()
            code_template = ''
            lines[0] = lines[0].format(node_name.lower())

            for line in lines:
                code_template = code_template + line

        return code_template

    def select(self, obj, value):
        if value and self.touch.button == 'right':
            self.selected = value[0].split('\\')[-1]
            self.add_widget(
                RightClickMenu(pos_hint={'x': self.touch.spos[0], 'top': self.touch.spos[1]},
                               size_hint=(None, None),
                               size=(300, 500),
                               funcs={'Export as Stacked': self.model_to_stacked})
            )
        return True

    def open_menu(self, obj, touch):
        if self.collide_point(*touch.pos):
            self.touch = touch

        return True
