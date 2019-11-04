from helpers import *
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np

# call the image and convert it into gray scale
oimage = Image.open("img.bmp").convert('LA')
oimage.save('gimg.png')

gim = plt.imread('gimg.png')
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

Q3 = [
    [17,18,24,47,99,99,99,99],
    [18,21,26,66,99,99,99,99],
    [24,26,56,99,99,99,99,99],
    [47,66,99,99,99,99,99,99],
    [99,99,99,99,99,99,99,99],
    [99,99,99,99,99,99,99,99],
    [99,99,99,99,99,99,99,99],
    [99,99,99,99,99,99,99,99]]
Q4= [
    [32,32,32,32,32,32,32,32],
    [32,32,32,32,32,32,32,32],
    [32,32,32,32,32,32,32,32],
    [32,32,32,32,32,32,32,32],
    [32,32,32,32,32,32,32,32],
    [32,32,32,32,32,32,32,32],
    [32,32,32,32,32,32,32,32],
    [32,32,32,32,32,32,32,32]
    ]
Q5= [
    [128,128,128,128,128,128,128,128],
    [128,128,128,128,128,128,128,128],
    [128,128,128,128,128,128,128,128],
    [128,128,128,128,128,128,128,128],
    [128,128,128,128,128,128,128,128],
    [128,128,128,128,128,128,128,128],
    [128,128,128,128,128,128,128,128],
    [128,128,128,128,128,128,128,128]
    ]
Q6= [
    [16,11,10,16,24,40,51,61],
    [12,12,14,19,26,58,60,55],
    [14,13,16,24,40,57,69,56],
    [14,17,22,29,51,87,80,62],
    [18,22,37,56,68,109,103,77],
    [24,35,55,64,81,104,113,92],
    [49,64,78,87,103,121,120,101],
    [72,92,95,98,112,100,103,99]
    ]

# def encode(frows,fcols,Q,gray):
Q=Q1
frame1D=np.zeros(frows*fcols)
finalvec=[]
for r in range(int(rows/frows)-1):
    for c in range(int(cols/fcols)-1):
        frame=gray[r:r+frows,c:c+fcols]
        DCTmat=DCT(frame) #it turned out that the frame of size 8 gets the least error when implementing DCT,the 4 and 16 stil get a relatively low error 
        quantize(DCTmat,Q)
        frame1D=zigzag(frame,frows)
        encoded=run_length(frame1D)
        
        finalvec.append(encoded)

finalvec=np.asarray(finalvec)

huffman = Huffman_encoding()
encoded_img = huffman.compress(finalvec)  #encoded message

    # return x,huffman

def decodecode(finalvec, huffman):
    recimage=np.zeros((rows,cols))# intialize recovered image
    decoded = huffman.decode_text(finalvec)
    decoded=reverse_run_length(decoded)# expand the runlength code
    
    for r in range(int(rows/frows)-1):
        for c in range(int(cols/fcols)-1):
            DCTmat1D=decoded[0:0+frows*fcols]#! still need modification
            DCTmat=invzig(frame1D)
            DCTmat=dequantize(DCTmat,Q)
            frame=IDCT(DCTmat)
            recimage[r:r+frows,c:c+fcols]=frame
    return recimage


quality=error(gray,recimage)