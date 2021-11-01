from torch.nn import Module, ModuleDict


class Net(Module):
    def __init__(self, interface=None, **kwargs):
        super(Net, self).__init__()
        self.nodes = interface.nodes()
        self.layers = ModuleDict()

        self.current_path = {'data': None,
                             'node': None}

        self.queue = []
        self.outputs = {}
        self.mapped_path = []

        # If `use_mapped` = 0 => using random node's path
        # Otherwise, when `use_mapped` = 1 => using mapped node's path
        self.use_mapped = 0

        # Add nodes as layers to the Module
        for node in self.nodes:
            # Format: `Node's name`: `Node's Algorithm`
            self.layers.update({node.name: node.algorithm()})
        # print(self.layers)

    # Add all needed nodes into a queue with the Input at index 0 and
    # Output at index len(self.queue)
    def initialize(self):
        for node in self.nodes:
            # print('Initialize', node.name, node.c_type)
            # node.rfo = 0

            if not self.use_mapped:
                if 'Input' in node.c_type:
                    self.queue.insert(0, node)

                elif 'Output' in node.c_type:
                    self.queue.insert(len(self.queue), node)

                else:
                    self.queue.insert(len(self.queue) - 1, node)
            else:
                self.queue = self.mapped_path

        # print(self.queue)

    # Zipping multiple inputs into 1 single list of inputs
    def zip_inputs(self, cted_nodes):
        # print('Zipping Inputs:', cted_nodes, len(cted_nodes))
        inputs = []

        for i in range(len(cted_nodes)):
            # print(cted_nodes[i])
            # print(self.outputs[cted_nodes[i]])
            inputs.insert(i, self.outputs[cted_nodes[i]])

        # print(inputs)
        return inputs

    # Add outputs to self.outputs
    def add_output(self, node, x):
        # x = (x)  # Cast to tuple for dynamic programming reason
        x = (*x,)
        n = len(x)  # Number of outputs

        for i in range(n):
            # print('Add Output:', node.name)
            self.outputs.update({node.name + ' ' + str(i): x[i]})
            # node.is_finished = True

    def remove_output(self, node):
        for output in self.outputs.keys():
            # print(node.name, output)
            if node.name in output:
                # print('Remove Output: ', node.name)
                self.outputs.pop(output)
                break

    def update_current_path(self, node, x):
        self.current_path['data'] = x
        self.current_path['node'] = node

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
        # print('Initialize Model\n')
        self.initialize()

        # Processing Input Node's output
        input_node = self.queue[0]

        x = self.layers[input_node.name](x)
        # Set Input Node's RFO (Ready For Output) = 1
        self.update_current_path(input_node, x)

        self.add_output(input_node, (x,))

        if not self.use_mapped:
            self.queue.pop(0)

            # Map Input and Output to self.mapped_path for faster processing
            self.mapped_path.insert(0, input_node)
            self.mapped_path.insert(1, self.queue)

        # print(self.queue)

        # print('\nStart Processing')
        # Process & Map other nodes to self.mapped_path
        while len(self.outputs) < len(self.nodes):
            for node in self.queue:
                try:
                    cted_nodes = node.connected_nodes

                    if self.is_existed_inputs(cted_nodes):
                        print(f'\nEnough Inputs To Process: {node.name}')
                        # print(self.outputs)
                        # print(cted_nodes)
                        if len(cted_nodes) == 1:
                            # print(x.size())
                            x = self.layers[node.name](x)

                        elif len(cted_nodes) > 1:
                            # print(len(self.zip_inputs(cted_nodes)))
                            x = self.layers[node.name](*self.zip_inputs(cted_nodes))

                        # print(type(x))
                        # print(f'Add Output: {node.name}')
                        if len(x) == 2 or len(x) == 3:
                            self.add_output(node, x)
                        else:
                            self.add_output(node, (x,))

                        # node.rfo = 1
                        self.update_current_path(node, x)

                        if not self.use_mapped:
                            self.queue.remove(node)

                            # if 'Output' not in node.c_type:
                            self.mapped_path.append(node)
                        # print('Close Node: ', node.name)

                except Exception as e:
                    # if 'size' in str(e):
                    #     raise e

                    # print('Cause: ', e)
                    # node.rfo = 0
                    self.queue.remove(node)
                    self.queue.insert(-2, node)

                    # raise e

            # print(len(self.outputs) < len(self.nodes))

        # if not self.use_mapped:
        #     # print('Use Mapped Path')
        #     self.queue = self.mapped_path
        #     self.use_mapped = 1
        #     # print([node.name for node in self.queue])

        self.use_mapped = 1
        self.outputs.clear()
        self.queue = self.mapped_path

        return x

        # for layer, node in zip(self.layers, self.nodes):
        #     cted_nodes = node.connected_nodes
        #
        #     for index in cted_nodes.keys():
        #         if len(cted_nodes) <= 1:
        #             x = self.layers[layer](x)
        #
        #         elif len(cted_nodes) > 1:
        #             x = self.layers[layer](*self.zip_inputs(cted_nodes))
        #
        #         self.add_output(node, index, x)

                # if len(cted_nodes) == 0:
                #     x = node.algorithm(x)
                #
                # elif len(cted_nodes) == 1:
                #     x = node.algorithm(*self.zip_inputs(cted_nodes))
                #
                # elif len(cted_nodes) > 1:
                #     x = node.algorithm(*self.zip_inputs(cted_nodes))

        # for block in self.blocks.keys():
        #     out = self.blocks[block](out)

        # return x