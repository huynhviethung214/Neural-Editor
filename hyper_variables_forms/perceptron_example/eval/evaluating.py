import torch
from utility.utils import record_graph, checkpoint, update_progress_bar, get_obj, breaker


def evaluating_alg(self, properties):
    get_obj(properties['interface'], 'ModeLabel').text = 'Mode: Evaluate'
    get_obj(properties['interface'], 'ProgressBar').max = properties['epochs']

    target = None
    pred = None

    with torch.no_grad():
        score = 0

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

            if target == pred:
                score += 1

        update_progress_bar(properties['interface'],
                            epoch + 1,
                            properties['epochs'])
