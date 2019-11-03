from helpers import *
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np

# call the image and convert it into gray scale

gim = plt.imread('2greyscale.png')
gray = rgb2gray(gim)

plt.imshow(gray, cmap=plt.get_cmap('gray'), vmin=0, vmax=1)

frows,fcols=8,8 #intialize the frame size
rows,cols=gray.shape
gim=fixdims(gim,frows,fcols) #fix image dimensions to make it multiple of the frame rows and columns

# quantiation tables

Q1=[[1,1,1,1,1,2,2,4],
    [1,1,1,1,1,2,2,4],
    [1,1,1,1,2,2,2,4],
    [1,1,1,1,2,2,4,8],
    [1,1,2,2,2,2,4,8],
    [2,2,2,2,2,4,8,8],
    [2,2,2,4,4,8,8,16],
    [4,4,4,4,8,8,16,16]]

Q2=[[1,2,4,8,16,32,64,128],
    [2,4,4,8,16,32,64,128],
    [4,4,8,16,32,64,128,128],
    [8,8,16,32,64,128,128,256],
    [16,16,32,64,128,128,256,256],
    [32,32,64,128,128,256,256,256],
    [64,64,128,128,256,256,256,256],
    [128,128,128,256,256,256,256,256]]

for r in range(int(rows/frows)-1):
    for c in range(int(cols/fcols)-1):
        frame=gray[r:r+frows,c:c+fcols]
        DCTmat=DCT(frame)
        quantize(DCTmat,Q1)
        twoD2oneD(frame)
        #performrunlength
        #performhuffman
        #indentover the final vector


print(DCTmat.shape)