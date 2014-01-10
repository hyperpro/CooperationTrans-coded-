'''
Created on 2014-1-10
@author: zhangxu
'''
from soliton import solition
import random
from math import ceil, floor
import sys
from pprint import pprint as pp

def ltcode(source, blocksize = 1024):
    random_dis = random.Random()
    n = len(source)     # Byte length of source file
    N = int(ceil(n/blocksize))  #the number of file block
    s = solition(N, random_dis.randint(0, 2**31 -1)) #degree distribution generation function
    while 1:
        d = next(s) #calculate the degree of ltcode
        seed = random_dis.randint(0, 2**31-1) #the seed of generating coding packets, for saving the space
        degree_random = random.Random(seed)
        r = bytearray(blocksize)
        for i in degree_random.sample(range(N), d):
            offset = i*blocksize
            j = 0
            end = min(n, blocksize+offset)
            while offset < end:
                r[j] ^= source[offset]
                offset = offset+1
                j = j+1
        yield {"degree": d, "seed": seed, "data": r}   
        

def edge_set(self):
    while len(self.edge):
        e = self.edge.pop()
        e.edge.remove(self)
        yield e
class original_node:
    def __init__(self, father, original_data, i, blocksize = 1024):
        self.father = father
        self.decode = False
        self.i = i
        self.edge = set()
        self.blocksize = blocksize
        offset = i*blocksize
        if offset+blocksize > father.n:
            end = father.n
        else:
            end = offset+blocksize
        
        self.data = memoryview(original_data)[i*blocksize:(i+1)*blocksize] ## out of memory?????????????????????________
                    
    def _decode(self):
        for i in edge_set(self):
            for j in range(self.blocksize):
                i.data[j] ^= self.data[j]
            if len(i.edge) == 1:
                i._decode()
                
class packet_decode:
    def __init__(self, father, original_nodes, N, blocksize, degree, seed, data):
        self.parent = father
        self.seed = seed # recovery the packets which are coded together
        self.data = bytearray(data)
        self.edge = set()
        degree_random = random.Random(seed)
        for i in degree_random.sample(range(N), degree):
            if (original_nodes[i].decode):
                for j in range(blocksize):
                    self.data[j] = self.data[j]^original_nodes[i].data[j]
            else:  
                self.edge.add(original_nodes[i])
                original_nodes[i].edge.add(self)
        if len(self.edge) == 1 :
              self._decode()
           
    def _decode(self):
        temp = self.edge.pop()
        temp.edge.remove(self)
        if (temp.decode == False):
            temp.data[:] = self.data
            temp.decode = True
            self.parent.undecode -= 1
            temp._decode()
            
class lt_decode:
    def __init__(self, n, blocksize = 1024):
        self.blocksize =blocksize
        self.n = n
        self.N = int(ceil(n/blocksize))
        self.original_data =bytearray(self.N*blocksize) # save the original data
        self.undecode = self.N
        self.original_nodes = []
        for i in range(self.N):
            self.original_nodes.append(original_node(self, self.original_data, i, blocksize))
    def decode_packet(self, packet):
        packet_decode(self, self.original_nodes, self.N, self.blocksize, packet['degree'], packet['seed'],packet['data'])
    
if __name__ == '__main__':
    print('ltcode welcome')
    with open('test.mp3', 'rb') as f:
        buffer = f.read()
    fountain = ltcode(buffer, 512)
    decoder = lt_decode(len(buffer),512)
    while decoder.undecode > 0:
        print("There still {:d} packets are not decoded".format(decoder.undecode), end = '\n')
        temp = next(fountain)
        decoder.decode_packet(temp)
    with open('testtest','wb') as f1:
        temp_file = memoryview(decoder.original_data)[:decoder.n]
        f1.write(temp_file)
    print("All the packets are decoded.\n")