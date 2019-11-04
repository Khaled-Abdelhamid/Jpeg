import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
import math
import heapq
import os

def rgb2gray(rgb):
  # transforms RGB image into grayscale image , it takes an array with 3 channels and output a 2D array
    return np.dot(rgb[...,:3], [0.2989, 0.5870, 0.1140])

def square(img):
  rows,cols=img.shape
  if rows<=cols:
    return img[:,:rows]
  else:
    return img[:cols,cols]


def fixdims(img,frows,fcols): # fix the dimensions to make them multiples of the frame size
  # img , is the image array
  # frows is the number of rows for each frame
  # fcols is the number of columns for each frame
  
  rows,cols,_ =img.shape #get the original rows and colomns and discard the cannal dimension
  rows-=rows%frows
  cols-=cols%fcols
  img=img[:rows,:cols,:]
  return img

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

def quantize(DCTmat,Q):# the quantiztion function takes the DCT matrix and the quantization table then it performs elementwise divison then round it to nearst integer
  DCTmat=np.divide(DCTmat,Q)
  DCTmat=np.round(DCTmat)

def dequantize(DCTmat,Q):
  DCTmat=np.multiply(DCTmat,Q)

def error(oimg,nimg):
  #get the least square error 
  return np.sum(np.square(np.subtract(oimg,nimg)))

#########################################################################3
#zigzag transformation
def isValid(i, j,  N):
   if (i < 0 or i >= N or j >= N or j < 0):
       return False                            
   return True

def zigzag(arr,N):
#This is the code for the function which converts the 2D array to 1D array
#The idea here is that I considered the first column and the last row as the starting indexes of the diagonals of the 2D array
#The function is called zigzag and the inputs are the array and its size which is N and the ouput is the 1D arary

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

 ################################################################3
#inverse zigzag transformation

def invzig(arr):
  rows, cols = (int(math.sqrt(len(arr))), int(math.sqrt(len(arr)))) 
  result = [[0 for i in range(cols)] for j in range(rows)] 
  count = 0;
  for i in range(0,2*rows):
    if(i%2 == 0):
      x = 0;
      y = 0;
      if (i<rows):
        x = i;
      else:
        x = rows - 1;
      if (i<rows):
        y = 0;
      else:
        y = i - rows + 1;
      while (x >= 0 and y < rows):
        result[x][y] = arr[count];
        count = count +1;
        x = x - 1;
        y = y + 1;
    else:
      x = 0;
      y = 0;
      if (i<rows):
        x = 0;
      else:
        x = i - rows + 1;
      if (i<rows):
        y = i;
      else:
        y = rows - 1;
      while (x < rows and y >= 0):
        result[x][y] = arr[count];
        count = count +1;
        x = x + 1;
        y = y - 1;
  return result;



########################################
## run length
def run_length(st):

    #prob_0 = count_0 / len(st)
    #prob_1 = count_1 / len(st)

    
    #print(prob_0//prob_1)

    num_bits = 3
    list_1 = []
    encoded = []

    for i in range(len(st)):
        
        if(st[i]!=0):
            
            length = len(list_1)
            if(length > 0):
                q, r = divmod(length,2**num_bits - 1)

                for j in range(q):
                    encoded = encoded + [0] + [1 for j in range(num_bits)]

                if(r != 0):
                    encoded = encoded + [0] + [0 for j in range(num_bits - len(f'{r:0b}'))] +[int(x) for x in f'{r:0b}']
    

                list_1 = []
                encoded.append(st[i])
            else:
                encoded.append(st[i])
        else:
            list_1.append(0)

    length = len(list_1)
    if(length > 0):
        q, r = divmod(length,2**num_bits - 1)

        for j in range(q):
            encoded = encoded + [0] + [1 for j in range(num_bits)]

        if(r != 0):
            encoded = encoded + [0] + [0 for j in range(num_bits - len(f'{r:0b}'))] +[int(x) for x in f'{r:0b}']
    

        list_1 = []

    
    return encoded

########################################
## reverse run_length

def reverse_run_length(encoded):
    decoded = []
    flag = 0 # num_of_bits
    for i in range(len(encoded)):
        
        if (flag>0):
            flag -= 1
            continue

        elif(encoded[i] == 0):
            for j in range(encoded[i+1]*4+encoded[i+2]*2+encoded[i+3]*1):
                decoded.append(0)
            flag = 3

        elif(encoded[i] != 0):
            decoded.append(encoded[i])
    
    return decoded


########################################
## Huffman encoding

class node:
    def __init__(self, symbol, frequency):
        self.symbol = symbol
        self.freq = frequency
        self.left = None
        self.right = None


    def __lt__(self, other):
        if(other == None):
            return -1
        if(not isinstance(other, node)):
            return -1

        return self.freq > other.freq

class Huffman_encoding:
    def __init__(self):
        self.heap = []
        self.codes = {}
        self.reverse_mapping = {}

    def make_freq_dict(self, message):
        frequency = {}
        for symbol in message:
            if not symbol in frequency:
                frequency[symbol] = 0
          
            frequency[symbol] += 1
        
        return frequency


    def build_heap(self, frequency):
        for key in frequency:
            n = node(key, -frequency[key])
            heapq.heappush(self.heap, n)

    def merge_nodes(self):
        while(len(self.heap)> 1):
            node_1 = heapq.heappop(self.heap)
            node_2 = heapq.heappop(self.heap)

            merged_node = node(None, node_1.freq + node_2.freq)
            merged_node.left = node_1
            merged_node.right = node_2

            heapq.heappush(self.heap, merged_node)


    def helper_function(self, root, code):
        if (root == None):
            return

        if (root.symbol != None):
            self.codes[root.symbol] = code
            self.reverse_mapping[code] = root.symbol
            return
        
        self.helper_function(root.left, code + "0")
        self.helper_function(root.right, code + "1")

    
    def make_codes(self):
        root = heapq.heappop(self.heap)
        code = ""
        self.helper_function(root, code)



    def get_encoded_message(self, message):
        encoded_message = ""
        for m in message:
            encoded_message += self.codes[m]

        return encoded_message



    def compress(self, message):
        #filename, file_extension = os.path.splitext(path)
        #output_path = filename + ".bin"

        # with open(path, 'r+') as file, open(output_path, 'wb') as output:
        #     message = file.read()
        #     message = message.rstrip()

        #     freq = self.make_freq_dict(message=message)
        #     self.build_heap(freq)
        #     self.merge_nodes()
        #     self.make_codes()

            # encoded_message = self.get_encoded_message(message)

            # print(encoded_message)

        freq = self.make_freq_dict(message=message)
        self.build_heap(freq)
        self.merge_nodes()
        self.make_codes()
        encoded_message = self.get_encoded_message(message)
        

        print("Compressed")
        return encoded_message    


    def decode_text(self, encoded_text):
        current_code = ""
        decoded_text = []

        for bit in encoded_text:
            current_code += bit
            if(current_code in self.reverse_mapping):
                character = self.reverse_mapping[current_code]
                decoded_text.append(character)
                current_code = ""

        return decoded_text























