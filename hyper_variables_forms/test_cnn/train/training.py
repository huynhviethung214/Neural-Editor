import torch
import numpy as np
from utility.utils import record_graph, checkpoint, breaker, update_progress_bar


@checkpoint
@record_graph
def training_alg(self, properties):
    losses = []
    np.random.shuffle(properties['dataset'])

    properties['model'].to(properties['device'])

    for epoch in range(properties['epochs']):
        epoch_loss = None

        for i, (im, label) in enumerate(properties['dataset']):
            breaker(self)

            im = im.reshape(1, 3, 300, 300)
            im = torch.FloatTensor(im).to(properties['device'])

            label = torch.LongTensor(label).to(properties['device'])

            output = properties['model'](im).to(properties['device'])
            output = output.reshape(1, -1).to(properties['device'])
            loss = properties['criterion'](output, label).to(properties['device'])
            epoch_loss = float(loss.item())

            properties['model'].zero_grad()
            loss.backward()
            properties['optimizer'].step()

        losses.append(epoch_loss)
        update_progress_bar(properties['interface'],
                            epoch,
                            properties['epochs'])

    # properties['obj']._evaluate(properties['eval_properties'],
    #                             properties['eval_properties']['eval_code'])

    if properties['is_save']:
        torch.save(properties['model'].state_dict(), 'weights/{0}.prmt'.format(properties['output_file_name']))
        torch.cuda.empty_cache()

    return losses, properties['epochs']
