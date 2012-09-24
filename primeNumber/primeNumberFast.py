# -*- coding: utf-8 -*-
from math import sqrt
import math
from numpy  import *
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
      
comm = MPI.COMM_WORLD
nprocs = comm.Get_size()
rank = comm.Get_rank()
      
t1 = time.time()
a=7
b=1000000

#if rank == 0:
#  try:
#    a=int(raw_input('Range A:'))
#    b=int(raw_input('Range B:'))
#  except ValueError:
#    print "Not a number"
   
a = comm.bcast(a, root=0)
b = comm.bcast(b, root=0)

l=(b-a)
jobPerProc=int(math.ceil(l/nprocs))
primenumbers= zeros(jobPerProc/2)
primeLenght=0
init=rank*jobPerProc + a;
if rank==(nprocs-1):
  end=b
else:
  end=init+jobPerProc
  
for i in range(init,end,1):
  if isprime(i):
    primenumbers[primeLenght]=i
    primeLenght=primeLenght+1
    #primenumbers=append(primenumbers,[i],axis=0)
    #print "Rank: ",rank," Number ",i	  
primenumbers = comm.gather(primenumbers, root=0)
amount= comm.reduce(primeLenght)
if rank == 0:
  print("%d Prime numbers found between  %d and %d.\n" % (amount, a, b))
#  print primenumbers
  t2 = time.time()
  print ("Time elapsed:")
  print (t2 - t1)