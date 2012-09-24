# -*- coding: utf-8 -*-
from math import sqrt
import math
from mpi4py import MPI
import time

def isprime(n):
      """Test if n is a prime number or not."""
      if n < 2:
          return False
      if n == 2:
          return True
      for i in range(2, int(math.ceil(math.sqrt(n)))+1):
          if n % i == 0:
              return False
      return True
      

      
t1 = time.time()
primenumbers=[]
a=7
b=1000000
for i in range(a,b,2):
	if isprime(i):
	  primenumbers.append(i)
	  #print i, len(primenumbers)
print("%d Prime numbers found between  %d and %d.\n" % (len(primenumbers), a, b))
t2 = time.time()
print ("Time elapsed:")
print (t2 - t1)