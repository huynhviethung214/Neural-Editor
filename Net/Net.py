import inspect
import logging
from termcolor import colored

from torch.nn import Module, ModuleDict


# logging.basicConfig(format='[%(created)f]: %(message)s', level=logging.DEBUG)


class Net(Module):
    def __init__(self, nodes=None, mapped_path=None, **kwargs):
        super(Net, self).__init__()
        self.nodes = nodes
        # print(self.nodes)
        self.interface = kwargs.get('interface')

        self.layers = ModuleDict()

        self.queue = [[], []]
        self.outputs = {}

        # If `use_mapped` = 0 => using random node's path
        # Otherwise, when `use_mapped` = 1 => using mapped node's path
        self.use_mapped = False

        self.mapped_path = mapped_path
        if not mapped_path:
            self.mapped_path = []
        else:
            self.use_mapped = True

        # Add nodes as layers to the Module
        for node_name in self.nodes.keys():
            # Format: `Node's name`: `Node's Algorithm`
            self.layers.update({node_name: self.nodes[node_name].algorithm()})
        # print(self.layers)

    # Add all needed nodes into a queue with the Input at index 0 and
    # Output at index len(self.queue)
    def initialize(self):
        logging.info('[Initialize][START]')

        for node_name in self.nodes.keys():
            if not self.use_mapped:
                layer_type = self.nodes[node_name].layer_get()

                if 'Input' in layer_type:
                    # logging.info(f'Initialize: [Input Node]: {node_name}')
                    self.queue.insert(1, self.nodes[node_name])

                elif 'Output' in layer_type:
                    # logging.info(f'Initialize: [Output Node]: {node_name}')
                    self.queue.insert(len(self.queue) - 1, self.nodes[node_name])

                else:
                    # logging.info(f'Initialize: [Hidden Node]: {node_name}')
                    self.queue.insert(2, self.nodes[node_name])
            else:
                self.queue = self.mapped_path

        for node in self.queue:
            if not node:
                self.queue.remove([])
        # logging.info(colored('INITIALIZE: [QUEUE]', 'blue') + f'{self.queue}')
        logging.info('[Initialize][END]')

    # Zipping multiple inputs into 1 single list of inputs
    def zip_inputs(self, cted_nodes):
        inputs = []

        for i, cted_node in enumerate(cted_nodes):
            logging.info(f'PACKING INPUT(S): {cted_node}')
            inputs.insert(i, self.outputs[cted_node])

        # logging.info(colored('SIZE OF INPUT', 'green') + f': [{len(inputs)}]')
        return inputs

    # Add outputs to self.outputs
    def add_output(self, node, x):
        # x = (x)  # Cast to tuple for dynamic inputs processing
        x = (*x,)
        n = len(x)  # Number of outputs

        for i in range(n):
            self.outputs.update({f'{node.name} Output {str(i)}': x[i]})
        # logging.info(f'OUTPUT: Number of outputs: {len(self.outputs)}')

    def remove_output(self, node):
        for output in self.outputs.keys():
            if node.name in output:
                self.outputs.pop(output)
                break

    def is_existed_inputs(self, cted_nodes):
        count = 0

        for cted_node in cted_nodes:
            for key in self.outputs.keys():
                if cted_node == key:
                    count += 1
                    break

        if count == len(cted_nodes):
            return 1
        return 0

    def get_connected_nodes(self, node):
        connected_nodes = []

        for node_link in node.inputs:
            tag = f'{node.name} {node_link.name}'
            target_tag = self.interface.node_links[tag].schema_get('target')
            connected_nodes.append(target_tag)
            # print(target.node.name)

        return connected_nodes

    def forward(self, x):
        logging.info('[FORWARD][START]')
        self.initialize()
        # print(f'Forward: {self.queue}')

        # Remove empty array in `self.queue`
        # Processing Input Node's output
        input_node = self.queue[0]
        logging.info(f'Input Node: {input_node.name}')
        x = self.layers[input_node.name](x)

        self.add_output(input_node, (x,))
        logging.info(f'ADD OUTPUT: {input_node.name}')

        if not self.use_mapped:
            self.queue.pop(0)

            # Map Input and Output to self.mapped_path for later processing
            self.mapped_path.insert(0, input_node)
            self.mapped_path.insert(1, self.queue)

        # Process & Map other nodes to self.mapped_path
        while len(self.outputs) < len(self.nodes.keys()):
            for node in self.queue:
                try:
                    cted_nodes = self.get_connected_nodes(node)

                    if self.is_existed_inputs(cted_nodes):
                        # x = self.layers[node.name](*self.zip_inputs(cted_nodes))

                        # if len(cted_nodes) == 1:
                        #     # logging.info(f'FORWARD: [INPUT\'S SIZE]: {len(x)}')
                        #     x = self.layers[node.name](*self.zip_inputs(cted_nodes))

                        if len(cted_nodes) >= 1:
                            # logging.info(f'FORWARD: [INPUT\'S SIZE]: {len(x)}')
                            x = self.layers[node.name](*self.zip_inputs(cted_nodes))

                        if len(x) == 2 or len(x) == 3:
                            self.add_output(node, x)
                        else:
                            self.add_output(node, (x,))

                        logging.info(f'FORWARD: {node.name}')
                        logging.info(f'ADD OUTPUT: {node.name}')

                        if not self.use_mapped:
                            self.queue.remove(node)
                            self.mapped_path.append(node)

                except Exception as e:
                    # logging.warning(f'EXCEPTION: \"{e}\" at \"{node.name}\"')
                    self.queue.remove(node)
                    self.queue.insert(-2, node)

        self.use_mapped = True
        self.outputs.clear()

        # Temporary disabling mapped path for training model
        if self.interface:
            # self.interface.mapped_path = self.queue = self.mapped_path
            self.interface.is_trained = True
            # self.interface.str_mapped_path = [node.name for node in self.mapped_path if node != []]

        logging.info('FORWARD: [END]')
        return x
