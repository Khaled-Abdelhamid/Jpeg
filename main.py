from helpers import *
import run_length
import huffman
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np

# call the image
oimage = Image.open("1.bmp").convert('LA')
oimage.save('1gray.png')
gim=plt.imread('1gray.png')
plt.imshow(gim[:,:,:3])

frows,fcols=8,8 #intialize the frame size

gim=fixdims(gim,frows,fcols) #fix image dimensions to make it multiple of the frame rows and columns

