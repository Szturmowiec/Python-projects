from pylab import *

lista=[]
f=open("dane","r")
for i in f: lista.append(i.split()[0])
f.close()
plot(lista)
savefig("wykres.png")