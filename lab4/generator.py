import string

def podz(n):
	for i in range(1,n+1):
		if n%i==0:
			yield i

def prime():
	n=2
	l=[2]
	yield 2
	while True:
		n+=1
		for i in l:
			if n%i==0: break
		else:
			l.append(n)
			yield n

def rozk(n):
	for p in prime():
		while n%p==0:
			n=n//p
			yield p
		if n==1: break

def gen(n):
	if n==0: yield ""
	else:
		for x in gen(n-1):
			yield x+'0'
			yield x+'1'

def gen2(k,s):
	if k==0: yield ""
	else:
		for x in gen2(k-1,s):
			for y in s:
				yield x+y

def perm(s):
	if len(s)==1: yield s
	else:
		for p in perm(s[1:]):
			for i in range(len(s)):
				yield p[:i]+s[0]+p[i:]

def komb(s,k):
	if k==1:
		for e in s: yield e
	elif k==len(s): yield s
	else:
		for x in komb(s[1:],k-1): yield s[0]+x
		for x in komb(s[1:],k): yield x

def war(s,k):
	for kom in komb(s,k):
		for p in perm(kom): yield p

k=120
g=(n for n in range(1,k+1) if k%n==0)
for i in g: print(i)
l=[n for n in rozk(120)]
print(l)

for i in gen(5): print(i)
#for i in gen2(7,"WIETnam"): print(i)
#for i in perm("WIETnam"): print(i)
#for i in perm(["aaa","bbb","ccc"]): print(i)

for i in komb("abcd",3): print(i)
for i in war("abcd",3): print(i)