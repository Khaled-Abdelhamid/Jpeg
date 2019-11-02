import heapq
import os

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



    def compress(self, path):
        filename, file_extension = os.path.splitext(path)
        output_path = filename + ".bin"

        with open(path, 'r+') as file, open(output_path, 'wb') as output:
            message = file.read()
            message = message.rstrip()

            freq = self.make_freq_dict(message=message)
            self.build_heap(freq)
            self.merge_nodes()
            self.make_codes()

            encoded_message = self.get_encoded_message(message)

            print(encoded_message)

        print("Compressed")
        return output_path
    



test = Huffman_encoding()
test.compress("in.txt")