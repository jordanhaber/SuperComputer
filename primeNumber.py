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
      
if self.rank!=0:
  a=7
  b=1000000
  l=(b-a)
  jobPerProc=int(math.ceil(l/self.rank_max))
  primenumbers= []#zeros(jobPerProc/2)
  primeLenght=0
  init=self.rank*jobPerProc + a;
  if self.rank==(self.rank_max-1):
    end=b
  else:
    end=init+jobPerProc
    
  for i in range(init,end,1):
    if isprime(i):
      #primenumbers[primeLenght]=i
      primenumbers.append(i)
      primeLenght=primeLenght+1
  self.solution.append(primenumbers)
if self.rank == 0:
#  print("%d Prime numbers found between  %d and %d.\n" % (amount, a, b))
  print self.solution


 
