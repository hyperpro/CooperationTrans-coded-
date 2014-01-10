'''
Created on 2014-1-10
@author: zhangxu
'''

import socket
import argparse
from pprint import pprint as pp
from ltcode import * 
from struct import *
import sys

BUF_SIZE=8120
DATA_SIZE=1024

def server(ns):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((ns.host, ns.port))
    with open(ns.filename,'rb') as f:
        buffer = f.read()
    sender = ltcode(buffer, DATA_SIZE)
    sys.setrecursionlimit(100000) #increase system stack
    while True:
        msg, a = s.recvfrom(BUF_SIZE)
        print("Server received {} bytes from {}:{}".format(len(msg), a[0], a[1]))
        print("Server start....")
        
        while 1:
            packet = next(sender)
            s.sendto(pack('!II'+str(DATA_SIZE)+'s', packet['degree'], packet['seed'], packet['data']),a)   

    
def client(ns):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    receiver = lt_decode(ns.length, DATA_SIZE)
    s.sendto(b'Hello', (ns.host, ns.port))
    sys.setrecursionlimit(100000)#increase system stack


    total_packet = 0
    while receiver.undecode > 0:
        total_packet += 1
        packet, a = s.recvfrom(BUF_SIZE)
        degree, seed, data = unpack('!II'+str(DATA_SIZE)+'s',packet)
        receiver.decode_packet({'degree':degree, 'seed':seed, 'data':data})
        print("There are {:d} packets. There are {:d} packets which are not decoded".format(total_packet, receiver.undecode))
    with open(ns.filename, 'wb') as f:
        o = memoryview(receiver.original_data)[:ns.length]
        f.write(o)
    
       
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', action='store_true', default=False, dest = 'server')
    parser.add_argument('-H', default='', dest='host')
    parser.add_argument('-P', default=50000, dest='port')
    parser.add_argument('-l', '--length', dest='length', type=int)
    parser.add_argument('-f', default='', type = str, dest = 'filename')
    parser.add_argument('msg', nargs='?')
    netService = parser.parse_args()
    if netService.server:
        server(netService)
    else:
        client(netService)