def evaluating_alg(self, properties):
    # Reset ProgressBar value to 0
    properties['obj'].value = 0

    # Your code goes here

    # Update ProgressBar value to 100 then terminated the current thread
    properties['obj']._update(100, 'Eval')
    properties['obj'].kill_process()
