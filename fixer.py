import os

path = 'D:\\datasets\\CNN\\datasets\\training_set'
files = os.listdir(path)

for file in files:
	_path = path + '\\{0}'.format(file)
	for im in os.listdir(_path):
		old_file = os.path.join(_path, im)
		im = im.split('.')[0] + '_' + im.split('.')[1] + '.jpg'
		new_file = os.path.join(_path, im)
		# _path = path + '\\{0}\\{1}.jpg'.format(file, im)
		os.rename(old_file, new_file)
