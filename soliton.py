'''
Created on 2014-1-10
@author: zhangxu
'''
from __future__ import print_function, division
from math import ceil
import random

def solition(N, seed):
    random_distri = random.Random()
    random_distri.seed(seed)
    while 1:
        x = random.random() #degree distribution
        i = int(ceil(1/x))
        yield i if i<=N else 1
    
if __name__ == '__main__':
    print('Hello')
    N = 10
    T = 10 ** 5
    f = [0]*N
    s = solition(N, random.randint(0, 2 ** 32 - 1))
    for i in range(T): #check the degree distribution with the scale of T
        j = next(s)
        f[j-1] += 1
        
    print(f) #we could observe that degree 2 and 3 has the most quantity.
    
    
    