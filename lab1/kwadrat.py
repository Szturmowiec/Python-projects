from math import sqrt
#import math
#import math as m

a=float(input("a="))
b=float(input("b="))
c=float(input("c="))
d=b*b-4*a*c

if d>=0:
  p=sqrt(d)
  #math.sqrt(d)
  x1=(-b-p)/(2*a)
  x2=(-b+p)/(2*a)
  print("x1={:0.2f}".format(x1))
  print("x2=%0.2f"%x2)
else:
  print("Brak rozw")