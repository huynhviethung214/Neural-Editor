from torch.nn import Module, ModuleDict


class Net(Module):
    def __init__(self, nodes=None, mapped_path=None, **kwargs):
        super(Net, self).__init__()
        self.nodes = nodes
        # print(self.nodes)
        self.interface = kwargs.get('interface')

        self.layers = ModuleDict()

        self.queue = []
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
        for node in self.nodes:
            # Format: `Node's name`: `Node's Algorithm`
            self.layers.update({node.name: node.algorithm()})
        # print(self.layers)

    # Add all needed nodes into a queue with the Input at index 0 and
    # Output at index len(self.queue)
    def initialize(self):
        # print(f'Nodes: {self.nodes}, Use mapped?: {self.use_mapped}')
        for node in self.nodes:
            if not self.use_mapped:
                if 'Input' in node.c_type:
                    # print('Input ', node.name)
                    self.queue.insert(0, node)

                elif 'Output' in node.c_type:
                    # print('Output ', node.name)
                    self.queue.insert(len(self.queue), node)

                else:
                    # print(node.name)
                    self.queue.insert(len(self.queue) - 1, node)
            else:
                self.queue = self.mapped_path

    # Zipping multiple inputs into 1 single list of inputs
    def zip_inputs(self, cted_nodes):
        inputs = []

        for i in range(len(cted_nodes)):
            inputs.insert(i, self.outputs[cted_nodes[i]])

        # print(inputs)
        return inputs

    # Add outputs to self.outputs
    def add_output(self, node, x):
        # x = (x)  # Cast to tuple for dynamic inputs processing
        x = (*x,)
        n = len(x)  # Number of outputs

        for i in range(n):
            self.outputs.update({node.name + ' ' + str(i): x[i]})

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

        if count == len(cted_nodes):
            return 1
        return 0

    def forward(self, x):
        self.initialize()
        # print(f'Forward: {self.queue}')

        if [] in self.queue:
            self.queue.remove([])

        # Processing Input Node's output
        input_node = self.queue[0]
        # print(f'Input: {self.layers[input_node.name]}')
        x = self.layers[input_node.name](x)

        self.add_output(input_node, (x,))

        if not self.use_mapped:
            self.queue.pop(0)

            # Map Input and Output to self.mapped_path for faster processing
            self.mapped_path.insert(0, input_node)
            self.mapped_path.insert(1, self.queue)

        # Process & Map other nodes to self.mapped_path
        while len(self.outputs) < len(self.nodes):
            for node in self.queue:
                try:
                    cted_nodes = node.connected_nodes
                    # print(self.layers[node.name])

                    if self.is_existed_inputs(cted_nodes):
                        if len(cted_nodes) == 1:
                            x = self.layers[node.name](x)

                        elif len(cted_nodes) > 1:
                            x = self.layers[node.name](*self.zip_inputs(cted_nodes))

                        if len(x) == 2 or len(x) == 3:
                            self.add_output(node, x)
                        else:
                            self.add_output(node, (x,))

                        if not self.use_mapped:
                            self.queue.remove(node)

                            self.mapped_path.append(node)

                except Exception as e:
                    self.queue.remove(node)
                    self.queue.insert(-2, node)

        self.use_mapped = False
        self.outputs.clear()

        # Temporary disabling mapped path for training model
        if self.interface:
            # self.interface.mapped_path = self.queue = self.mapped_path
            self.interface.is_trained = True
            # self.interface.str_mapped_path = [node.name for node in self.mapped_path if node != []]

        return x
