import matplotlib.pyplot as plt
from PIL import Image
import numpy as np

def rgb2gray(rgb):
    return np.dot(rgb[...,:3], [0.2989, 0.5870, 0.1140])

def fixdims(img,frows,fcols): # fix the dimensions to make them multiples of the frame size
  rows,cols,_ =img.shape #get the original rows and colomns and discard the cannal dimension
  rows-=rows%frows
  cols-=cols%fcols
  img=img[:rows,:cols,:]
  return img



def getbasis(u,v,brows,bcols):#helper function to get the basis that will be used in DCT
  basis=np.zeros((brows,bcols))
  for i in range(brows):
    for j in range(bcols):
      basis[i,j]=np.cos((2*i+1)*u*np.pi/16)*np.cos((2*j+1)*v*np.pi/16)
  return basis

def DCT(frame):
  frows,fcols=frame.shape
  DCTmat=np.zeros((frows,fcols))
  for u in range(frows):
    for v in range(fcols):
      basis=getbasis(u,v,frows,fcols)
      DCTmat[u,v]=np.sum(np.multiply(basis,frame))#the correlation operation
  #scaling operations to remove energy at the first rows
  DCTmat[0,:]/=32
  DCTmat[:,0]/=32
  DCTmat[0,0]*=16
  DCTmat[1:,1:]/=16
  return DCTmat

def IDCT(DCTmat):#the function multipy each basis with the corresponding scale and adds them up
  frows,fcols=DCTmat.shape
  frame=np.zeros((frows,fcols))
  for u in range(frows):
    for v in range(fcols):
      basis=getbasis(u,v,frows,fcols)
      frame+=DCTmat[u,v]*basis
  return frame

def quantize(DCTmat,Q):
  DCTmat=np.divide(DCTmat,Q)
  DCTmat=np.round(DCTmat)

def dequantize(DCTmat,Q):
  DCTmat=np.multiply(DCTmat,Q)

def error(oimg,nimg):
  return np.sum(np.square(np.subtract(oimg,nimg)))

def isValid(i, j,  N):
   if (i < 0 or i >= N or j >= N or j < 0):
       return False                             # Learned that true and false have to start with capitals
   return True

def diagonal(arr,N):
#This is the code for the function which converts the 2D array to 1D array
#The idea here is that I considered the first column and the last row as the starting indexes of the diagonals of the 2D array
#The function is called diagonal and the inputs are the array and its size which is N and the ouput is the 1D arary

  One_D_array = []
  for k in range(0, N) :
    flippedd = []
    if(k%2!=0):                                      # If the index of the coulmn is odd
      flippedd.append(arr[k][0])
    else:
      One_D_array.append(arr[k][0])
    i=k-1; #setting row index to point to next point in the diagonal
    j=1;   #setting column index to point to next point in the diagonal

    if(k%2!=0):
      while (isValid(i, j, N)) :
        flippedd.append(arr[i][j])
        i -= 1 #Moving up accross the diagonal by increasing the column index and decreasing the row index
        j += 1
    else:
      while (isValid(i, j,N)) :
        One_D_array.append(arr[i][j])
        i -= 1 #Moving up accross the diagonal by increasing the column index and decreasing the row index
        j += 1
    flippedd.reverse()
    for z in range(len(flippedd)):
        One_D_array.append(flippedd[z])   #Learned that array index should be put between [] not ()
    del flippedd[:]

  for k2 in range(1,N):
    flipped2 =[]
    if(k2 % 2==0):
      flipped2.append(arr[N-1][k2])
    else:
      One_D_array.append(arr[N-1][k2])
    i = N - 2
    j = k2 + 1

    if(k%2==0):
      while (isValid(i, j,N)) :
        flipped2 = []
        flipped2.append(arr[i][j])
        i -= 1 #Moving up accross the diagonal by increasing the column index and decreasing the row index
        j += 1
    else:
      while (isValid(i, j,N)) :
        One_D_array.append(arr[i][j])
        i -= 1 #Moving up accross the diagonal by increasing the column index and decreasing the row index
        j += 1
    flipped2.reverse()
    for z in range(len(flipped2)):
      One_D_array.append(flipped2[z])
    del flipped2[:]
  return One_D_array

