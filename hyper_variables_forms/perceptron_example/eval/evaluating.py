import torch
from utility.utils import record_graph, checkpoint, update_progress_bar, get_obj, breaker


def evaluating_alg(self, properties):
    get_obj(properties['interface'], 'ModeLabel').text = 'Mode: Evaluate'
    accuracies = []

    with torch.no_grad():
        epoch_accuracy = 0

        for epoch in range(properties['epochs']):
            for X, y in properties['dataset']:
                breaker(self)

                X = torch.Tensor(X)
                y = torch.Tensor(y)
                X = X.to(properties['device'])
                y = y.to(properties['device'])

                output = properties['model'](X).to(properties['device']).view(-1)
                pred = torch.argmax(output)

                target = y.tolist()[0]
                pred = pred.item()
                # epoch_accuracy = properties['criterion'](pred, target)

                update_progress_bar(properties['obj'],
                                    epoch + 1,
                                    properties['epochs'])

        # accuracies.append(epoch_accuracy)
        update_progress_bar(properties['obj'],
                            epoch + 1,
                            properties['epochs'])

    # return accuracies, properties['epochs']
