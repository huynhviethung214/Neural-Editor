import torch


def training_alg(self, properties):
    for epoch in range(1, properties['epochs']):
        for X, y in properties['dataset']:
            if self.end_task:
                print('End Task')
                return

            X = torch.FloatTensor(X)
            y = torch.FloatTensor(y)

            X = X.to(properties['device'])
            y = y.to(properties['device'])

            # print(epoch / properties['epochs'] * 100)

            properties['model'].zero_grad()
            properties['optimizer'].zero_grad()

            output = properties['model'](X).to(properties['device'])
            loss = properties['criterion'](output, y)

            loss.backward()
            properties['optimizer'].step()

    properties['obj']._evaluate(properties['eval_properties'],
                                properties['eval_properties']['eval_code'])

    if properties['is_save']:
        torch.save(properties['model'].state_dict(),
                   '{0}\\{1}.prmt'.format(properties['weight_path'],
                                          properties['output_file_name']))
        torch.cuda.empty_cache()
