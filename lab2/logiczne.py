import string
VAR=string.ascii_lowercase
OP="&|>"

def spr(w):
  ln=0
  st=True
  for z in w:
  	if st:
  	  if z in VAR:
  	  	st=False
  	  elif z in ")"+OP:
  	  	return False
  	else:
  	  if z in OP:
  	  	st=True
  	  elif z in VAR+"(":
  	  	return False
  	if z=="(": ln+=1
  	if z==")": ln-=1
  	if ln<0: return False
  return not st and ln==0

def bal(w,op):
  ln=0
  for i in range(len(w)-1,0,-1):
  	if w[i]==")": ln-=1
  	if w[i]=="(": ln+=1
  	if w[i] in OP and ln==0: return i
  return -1

def onp(w):
  while w[0]=="(" and w[-1]==")" and spr(w[1:-1]):
  	w=w[1:-1]
  p=bal(w,">")
  if p>=0:
  	return onp(w[:p])+onp(w[p+1:])+w[p]
  p=bal(w,"&|")
  if p>=0:
  	return onp(w[:p])+onp(w[p+1:])+w[p]
  return w

def var(w):
  return "".join(sorted(set(w)&set(VAR)))

def mapuj(w,zm,val):
  l=list(w)
  for i in range(len(l)):
    p=zm.find(l[i])
    if p>=0: l[i]=val[p]
  return "".join(l)

def OR(a,b): return a or b

def AND(a,b): return a and b

def IMPL(a,b): return not a or b

def gen(n):
  for i in range(2**n):
  	yield bin(i)[2:].rjust(n,"0")

def value(w,val):
  v=var(w)
  w=mapuj(w,v,val)
  st=[]
  for z in w:
    if z in "01": st.append(int(z))
    elif z=="|": st.append(OR(st.pop(),st.pop()))
    elif z=="&": st.append(AND(st.pop(),st.pop()))
    elif z==">": st.append(IMPL(st.pop(),st.pop()))
  return st.pop()

while True:
  w=input(">>")
  if spr(w):
  	v=var(w)
  	print("zmienne: ",v)
  	wonp=onp(w)
  	print("onp: ",wonp)
  	for x in gen(len(v)):
  	  print(x,value(wonp,x))
  else:
  	print("error")