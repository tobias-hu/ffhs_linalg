import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from scipy.fftpack import dct, idct
from skimage import data
# 'cause of some weird issues with the matplotlib backend
matplotlib.use('TkAgg')

img = data.brick()

plt.imshow(img, cmap='gray')
plt.show()

dctRows = dct(img, axis=1, norm='ortho')

dctCols = dct(dctRows, axis=0, norm='ortho')
print(dctCols)

plt.imshow(np.log(np.abs(dctCols)), cmap='gray')

plt.show()

idctCols = idct(dctCols, axis=0, norm='ortho')
idctImg = idct(idctCols, axis=1, norm='ortho')

plt.imshow(idctImg, cmap='gray')
plt.show()
