import torch
import numpy as np
import gc


def training_alg(self, properties):
    np.random.shuffle(properties['dataset'])

    properties['model'].to(properties['device'])

    for epoch in range(properties['epochs']):

        # properties['obj']._update((epoch / properties['epochs']) * 100, 'Train')

        for i, (im, label) in enumerate(properties['dataset']):
            if self.end_task:
                # print(gc.get_count())
                # gc.collect()
                # print(gc.get_count())
                print('End Task')
                return

            im = im.reshape(1, 3, 300, 300)
            im = torch.FloatTensor(im).to(properties['device'])

            label = torch.LongTensor(label).to(properties['device'])

            output = properties['model'](im).to(properties['device'])
            loss = properties['criterion'](output, label).to(properties['device'])

            properties['model'].zero_grad()
            loss.backward()
            properties['optimizer'].step()

    # properties['obj']._evaluate(properties['eval_properties'],
    #                             properties['eval_properties']['eval_code'])

    if properties['is_save']:
        torch.save(properties['model'].state_dict(), '{0}.prmt'.format(properties['output_file_name']))
        torch.cuda.empty_cache()

    # print('END')
