def sp(n):
  sum=1
  p=2
  while  p*p<n:
    if n%p==0: sum=sum+p+n//p
    p+=1
  #end while
  if p*p==n: sum+=p
  return sum
#end def

if __name__=="__main__":
  for i in range(1,30):
    if sp(i)==i: print(i)
  #end for
#end if