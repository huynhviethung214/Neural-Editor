from PIL import Image
import numpy as np


im = Image.open('D:\Ruby Projects\everything-cheaper\\app\\assets\images\companies\\amazon.png')
im = im.convert('RGBA')

data = np.array(im)   # "data" is a height x width x 4 numpy array
red, green, blue, alpha = data.T # Temporarily unpack the bands for readability

# Replace white with red... (leaves alpha values alone...)
white_areas = (red <= 255) & (blue <= 255) & (green <= 255) & (red >= 250) & (green >= 250) & (blue >= 250)
data[..., :-1][white_areas.T] = (254, 251, 233) # Transpose back needed

im2 = Image.fromarray(data)
# im2.show()

im2.save('D:\Ruby Projects\everything-cheaper\\app\\assets\images\companies\\amazon.png')
