from sump import sp
for i in range(1,10000):
  j=sp(i)
  k=sp(j)
  if i==k and i!=j:
    print(i,j)
  #end if
#end for