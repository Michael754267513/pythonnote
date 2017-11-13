from PIL import Image
import numpy as np
from pylab import *
ImageTest = np.array(Image.open("1.jpg"))
# IM.tofile("pic", sep=",")
print(ImageTest.shape, ImageTest.itemsize, ImageTest.dtype, ImageTest.ndim)
ImArry = [255, 255, 255] - ImageTest
im1 = Image.fromarray(ImArry.astype('uint8'))
im1.save("pic1.jpg")

