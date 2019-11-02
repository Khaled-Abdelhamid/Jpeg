# import math
# import numpy as np

def run_length(st):
    count_0 = st.count(0)

    #prob_0 = count_0 / len(st)
    #prob_1 = count_1 / len(st)

    
    #print(prob_0//prob_1)

    num_bits = 3
    list_1 = []
    list_2 = []
    encoded = []
    counter = 0
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



# m = [1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
# print(run_length(m))



