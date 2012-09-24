# -*- coding: utf-8 -*-
from math import sqrt
import math
from numpy  import *
from mpi4py import MPI
import time

t1 = time.time()

input = open('small.txt', 'r')
text = input.read()
wordlist = text.split()

wordfreq = [wordlist.count(p) for p in wordlist]

dictionary = dict(zip(wordlist,wordfreq))
aux = [(dictionary[key], key) for key in dictionary]
aux.sort()
aux.reverse()
for a in aux: print a

t2 = time.time()
print ("Time elapsed:")
print (t2 - t1)