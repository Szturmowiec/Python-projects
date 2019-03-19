import string

def connect(s1,s2):
	res=""
	lr=0
	for i,j in zip(s1,s2):
		if i==j: res+=i
		else: res+="-"; lr+=1
	if lr==1: return res
	return False

def reduce(dane):
	res=set()
	r=False
	for i in dane:
		x=False
		for j in dane:
			wyn=connect(i,j)
			if wyn: res.add(wyn); x=True; r=True
		if not x: res.add(i)
	if r: return reduce(res)
	return res

def reudce2(d1,d2,i,j):
	t=[[0 for x in range(i)] for y in range(j)]
	

def wypisz(s):
	wyn=""
	for i in s:
		res=""
		for a,b in zip(i,string.ascii_lowercase[:len(i)]):
			if a=="0": res+="~"+b+"&"
			elif a=="1": res+=b+"&"
		wyn+="("+res[:-1]+")|"
	return wyn[:-1]

f=open("dane")
dane=set(f.read().split())
f.close()
dane2=reduce(dane)
print(wypisz(reduce2(dane,dane2,len(dane),len(dane2))))