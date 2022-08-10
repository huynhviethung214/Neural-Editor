# import os
#
# path = 'D:\\datasets\\CNN\\datasets\\training_set'
# files = os.listdir(path)
#
# for file in files:
# 	_path = path + '\\{0}'.format(file)
# 	for im in os.listdir(_path):
# 		old_file = os.path.join(_path, im)
# 		im = im.split('.')[0] + '_' + im.split('.')[1] + '.jpg'
# 		new_file = os.path.join(_path, im)
# 		# _path = path + '\\{0}\\{1}.jpg'.format(file, im)
# 		os.rename(old_file, new_file)


# import os
# from os import path
#
# fpath = 'D:\Python Projects\Project Alpha\dataset\Animals\\validate'
# categories = ['cat', 'dog', 'fox', 'tiger']
# i = 0
#
# for folder in os.listdir(fpath):
#     ims_path = path.join(fpath, folder)
#     for im in os.listdir(ims_path):
#         if folder not in im:
#             os.rename(path.join(ims_path, im), path.join(ims_path, f'{folder}{i}.jpg'))
#             i += 1


import pandas as pd

df = pd.read_csv("test.csv", sep="\t", header=None)

for i in range(df.shape[0]):
    #print(f"new Vector4({df[0][i]}f", end="")
    for j in range(1, df.shape[1]):
        print(f"{df[j][i]}, ", end="")
    #print("),")

