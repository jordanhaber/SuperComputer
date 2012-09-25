# -*- coding: utf-8 -*-
from math import sqrt
import math
from numpy  import *
from mpi4py import MPI
import time

def printDict(dictionary):
  aux = [(dictionary[key], key) for key in dictionary]
  aux.sort()
  aux.reverse()
  for a in aux: print a
 
def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1
  
comm = MPI.COMM_WORLD
nprocs = comm.Get_size()
rank = comm.Get_rank()
dictionary = dict()
if rank==0:  
  t1 = time.time()
  fileName = 'mid.txt'
  flen=file_len(fileName)
  file = open(fileName, 'r')
  txt=""
  cont=0  
  linesPerProc=int(math.ceil(flen/(nprocs-1)))
  destNumber=1
  print "The file has %d lines" % flen
  print "We are running %d procs" % nprocs
  print "Each proc will word on %d lines" % linesPerProc
  while 1:
    line = file.readline()
    txt += line
    if not line:
        break
    cont+=1
    if cont==linesPerProc:
      comm.send(txt, dest=destNumber)
      #print "Data sent to proc %d" %destNumber
      cont=0
      destNumber+=1
      txt=""
      if destNumber> (nprocs-1):
	destNumber=1
      
if rank != 0:
  print "Proc %d stated" % rank
  text = comm.recv(source=0)
  print "Proc %d received the lines" % rank
  wordlist = text.split()
  print "Proc %d splited the lines, word count: %d" % (rank,len(wordlist))
  #wordfreq = [wordlist.count(p) for p in wordlist]
  cont=0
  for p in wordlist:
    cont+=1
    dictionary[p]=wordlist.count(p)
    #print "Cont %d" %cont
  #print "Proc %d , word freq: %d" % (rank,len(wordfreq))
  #wordfreq=zeros(0)
  #dictionary = dict(zip(wordlist,wordfreq))
  #print "Proc %d dict created" % rank
dictionaries = comm.gather(dictionary, root=0)
if rank==0:  
  if nprocs>2 :
    for i in range(1,len(dictionaries)-1,1):
      dictionary= dict(dictionaries[i].items() + dictionaries[i+1].items())
  else:
    dictionary= dictionaries[1]
  printDict(dictionary)
  t2 = time.time()
  print ("Time elapsed:")
  print (t2 - t1)