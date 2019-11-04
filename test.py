import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
import math


# def getbasis(u,v,brows,bcols):#helper function to get the basis that will be used in DCT
#   # u,v is the location of the basis in the DCT matrics
#   # brows  the number of rows of the basis
#   # bcols  the number of columns of the basis 
#   basis=np.zeros((brows,bcols))
#   for i in range(brows):
#     for j in range(bcols):
#       basis[i,j]=np.cos((2*i+1)*u*np.pi/16)*np.cos((2*j+1)*v*np.pi/16)
#   return basis

# def DCT(frame):# performs discrete cosine transform, it takes the frame and outputs the DCT matrix
  
#   frows,fcols=frame.shape
#   DCTmat=np.zeros((8,8))
#   for u in range(8):
#     for v in range(8):
#       basis=getbasis(u,v,frows,fcols)
#       DCTmat[u,v]=np.sum(np.multiply(basis,frame))#the correlation operation
#   #scaling operations to remove energy at the first rows
#   DCTmat[0,:]/=32
#   DCTmat[:,0]/=32
#   DCTmat[0,0]*=16
#   DCTmat[1:,1:]/=16
#   return DCTmat

# def IDCT(DCTmat,frows,fcols):#the function multipy each basis with the corresponding scale and adds them up 
#   frame=np.zeros((frows,fcols))
#   for u in range(8):
#     for v in range(8):
#       basis=getbasis(u,v,frows,fcols)
#       frame+=DCTmat[u,v]*basis
#   return frame

# A=np.random.rand(55,55)
# dctmat=DCT(A)
# h=IDCT(dctmat,55,55)
# print(h.shape)
# print(h-A)



def getbasis(u,v,brows,bcols):#helper function to get the basis that will be used in DCT
  # u,v is the location of the basis in the DCT matrics
  # brows  the number of rows of the basis
  # bcols  the number of columns of the basis 
  basis=np.zeros((brows,bcols))
  for i in range(brows):
    for j in range(bcols):
      basis[i,j]=np.cos((2*i+1)*u*np.pi/16)*np.cos((2*j+1)*v*np.pi/16)
  return basis

def DCT(frame):# performs discrete cosine transform, it takes the frame and outputs the DCT matrix
  
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

A=np.random.rand(32,32)
dctmat=DCT(A)
h=IDCT(dctmat)
print(h.shape)
print(h-A)


  