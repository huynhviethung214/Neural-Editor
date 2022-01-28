import torch
import numpy as np
from utility.utils import record_graph, checkpoint, breaker


@checkpoint
@record_graph
def training_alg(self, properties):
    losses = []

    properties['model'].to(properties['device'])

    for epoch in range(properties['epochs']):
        # epoch_loss = None

        for i, (im, _) in enumerate(properties['dataset'].dataset):
            breaker(self)

            im = np.array(im).reshape(-1, 28 * 28)
            im = torch.FloatTensor(im).to(properties['device'])

            reconstruced = properties['model'](im).to(properties['device'])
            loss = properties['criterion'](reconstruced, im).to(properties['device'])
            epoch_loss = float(loss.item())

            properties['model'].zero_grad()
            loss.backward()
            properties['optimizer'].step()
            losses.append(epoch_loss)

    if properties['is_save']:
        torch.save(properties['model'].state_dict(), 'weights/{0}.prmt'.format(properties['output_file_name']))
        torch.cuda.empty_cache()

    return losses, properties['epochs']
