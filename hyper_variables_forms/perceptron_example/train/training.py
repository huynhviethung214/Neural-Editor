import torch
from utility.utils import record_graph, checkpoint, breaker, update_progress_bar, get_obj


@checkpoint
@record_graph
def training_alg(self, properties):
    get_obj(properties['interface'], 'ModeLabel').text = 'Mode: Train'
    losses = []

    for epoch in range(1, properties['epochs']):
        epoch_loss = None

        for X, y in properties['dataset']:
            breaker(self)

            X = torch.FloatTensor(X)
            y = torch.FloatTensor(y)

            X = X.to(properties['device'])
            y = y.to(properties['device'])

            properties['model'].zero_grad()
            properties['optimizer'].zero_grad()

            output = properties['model'](X).to(properties['device'])
            loss = properties['criterion'](output, y)
            epoch_loss = float(loss.item())

            loss.backward()
            properties['optimizer'].step()

        losses.append(epoch_loss)
        update_progress_bar(properties['obj'],
                            epoch + 1,
                            properties['epochs'])

    properties['obj']._evaluate(properties['eval_properties'],
                                properties['eval_properties']['eval_code'])

    if properties['is_save']:
        torch.save(properties['model'].state_dict(),
                   '{0}/{1}.prmt'.format(properties['weight_path'],
                                         properties['output_file_name']))
        torch.cuda.empty_cache()

    return losses, properties['epochs']
