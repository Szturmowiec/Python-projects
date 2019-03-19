import string
import sys
VAR=string.ascii_lowercase+"FT"
OP="^&|/>"

def spr(w):
  ln=0
  st=True
  for z in w:
  	if st:
  	  if z in VAR: #przy zmiennej stan false
  	  	st=False
  	  elif z in ")"+OP: #jak dla stanu true (operator) mamy od razu ) albo operator niebędący negacją, to wyrażenie złe
  	  	return False
  	else:
  	  if z in OP+"~": #przy operatorze stan true
  	  	st=True
  	  elif z in VAR+"(": #jak dla stanu false (zmienna) mamy kolejną albo od razu ( to wyrażenie jest złe
  	  	return False
  	if z=="(": ln+=1 #sprawdzamy czy nawiasy się zgadzają
  	if z==")": ln-=1
  	if ln<0: return False
  return not st and ln==0 #not st bo false jak kończymy na zmiennej a true jak na operatorze 

def remove_negation_space(w):
  wyn=""
  ile=0
  for i in range(len(w)):
    if (w[i]=="~"):
      ile+=1
    if (w[i]!="~" and w[i]!=" "):
      if (ile%2==1): wyn=wyn+"~"+w[i] #jak znak nie jest spacją, to go zachowujemy, usuwamy też nadmiarowe negacje
      else: wyn+=w[i]
      ile=0
  return wyn

def bal(w,op):
  ln=0
  for i in range(len(w)-1,0,-1):
    if w[i]==")": ln-=1
    if w[i]=="(": ln+=1
    if w[i] in OP and ln==0: return i #szukamy pozycji danego operatora
  return -1

def onp(w):
  while w[0]=="(" and w[-1]==")" and spr(w[1:-1]): #usuwamy zbędne nawiasy
    w=w[1:-1]
  p=bal(w,">")
  if p>=0:
    return onp(w[:p])+onp(w[p+1:])+w[p] #wyszukujemy operator i zamieniamy na onp (opereator idzie na koniec)
  p=bal(w,"&|/")
  if p>=0:
    return onp(w[:p])+onp(w[p+1:])+w[p] #wyszukiwanie kolejnych operatorów zgodnie z ich priorytetem wykonania (najmniejszy na koniec)
  p=bal(w,"^")
  if p>=0:
    return onp(w[:p])+onp(w[p+1:])+w[p]
  if w[0]=="~": return onp(w[1:])+w[0]
  return w

def var(w):
  return "".join(sorted(set(w)&set(VAR))) #tworzymy zbiór zmiennych danego wyrażenia

def mapuj(w,zm,val):
  l=list(w)
  for i in range(len(l)):
    p=zm.find(l[i])
    if p>=0: l[i]=val[p]
  return "".join(l)

def OR(a,b): return a or b

def AND(a,b): return a and b

def IMPL(a,b): return not a or b

def DYS(a,b): return not AND(a,b)

def XOR(a,b): return (a or b) and DYS(a,b)

def NEG(a): return not a

def gen(n): #generujemy ciągi binarne jako wartości zmiennych
  for i in range(2**n):
    yield bin(i)[2:].rjust(n,"0")

def value(w,val): #ewaluacja wyrażenia dla danych wartości zmiennych
  v=var(w)
  w=mapuj(w,v,val)
  st=[]
  for z in w: #odkłądamy na stos wartości zmiennych i wyniki operacji na nich
    if z in "01": st.append(int(z))
    elif z=="T": st.append(1)
    elif z=="F": st.append(0)
    elif z=="~": st.append(NEG(st.pop()))
    elif z=="^": st.append(XOR(st.pop(),st.pop()))
    elif z=="/": st.append(DYS(st.pop(),st.pop()))
    elif z=="|": st.append(OR(st.pop(),st.pop()))
    elif z=="&": st.append(AND(st.pop(),st.pop()))
    elif z==">": #przy implikacji ważna kolejność argumentów, a w onp wyżej na stosie jest drugi
      b=st.pop()
      a=st.pop()
      st.append(IMPL(a,b))
  return st.pop()

def connect(s1,s2): #sklejamy dwa ciągi w jeden w algorytmie Quina
  res=""
  lr=0
  for i,j in zip(s1,s2):
    if i==j: res+=i
    else: res+="-"; lr+=1
  if lr==1: return res #może być tylko jedna różnica
  return False

def reduce(dane): #sprawdzamy wszystkie pary ciągów i sklejamy co się da, wykonujemy tak długo, aż nic już nie można skleić
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

def check(a,b): #sprawdzamy czy dwa ciągi są identyczne z dokłądnością do "-"
  for i,j in zip(a,b):
    if i!=j and i!="-" and j!="-": return 0
  return 1

def reduce2(d,r,i,j): #druga część algorytmu quina - tworzymy tablicę z wierszami odp minimalnym iloczynom,
  res=set() #a kolumny ciągom dla których wartość jest 1
  t=[[0 for x in range(j)] for y in range(i)]
  for a in range(i):
    for b in range(j):
      t[a][b]=check(d[a],r[b]) #1 w tablicy pokazują, z połączenia jakich ciągóœ powstałd dany iloczyn
  for c in range(i):
    ile=0
    ind=0
    for d in range(j):
      if t[c][d]==1:
        ile+=1
        ind=d
    if ile==1: res.add(r[ind]) #jak w kolumniej jest tylko jedna 1, to iloczyn jest niezbędny, inaczej zostawiamy
    ile=0
  return res


def wypisz(s):
  wyn=""
  for i in s:
    res=""
    for a,b in zip(i,string.ascii_lowercase[:len(i)]):
      if a=="0": res+="~"+b+"&"
      elif a=="1": res+=b+"&"
    wyn+="("+res[:-1]+")|"
  return wyn[:-1]

def imp_dys(w): #zamieniamy na implikacje i dysjunkcje
  i=0
  st=[]
  while i<len(w): #w kolejnych warunkach możliwe ciągi znaków które można uprościć (onp)
    if w[i]=="~" and i<len(w)-3 and w[i+2]=="~" and w[i+3]=="|":
      st.append(st.pop()+w[i+1]+"/")
      i+=4
    elif w[i]=="~" and i<len(w)-2 and w[i+2]=="|":
      st.append(st.pop()+w[i+1]+">")
      i+=3
    elif w[i]=="~" and i<len(w)-1 and w[i+1]=="|":
      st.append(st.pop()+st.pop()+">")
      i+=2
    else:
      st.append(w[i])
      i+=1
  j=0
  wyn=""
  while j<len(st):
  	wyn+=st[j]
  	j+=1
  return wyn

def xory(w): #zamieniamy na xory
  i=0
  st=[]
  while i<len(w): #w kolejnych warunkach możliwe ciągi znaków które można uprościć (onp)
    if w[i]=="~" and i<len(w)-7 and w[i+1] in VAR and w[i+2]=="&" and w[i+3] in VAR and w[i+4] in VAR and w[i+5]=="~" and w[i+6]=="&" and w[i+7]=="|":
      st.append(st.pop()+w[i+1]+"^")
      i+=8
    elif w[i]=="~" and i<len(w)-6 and w[i+1]=="&" and w[i+2] in VAR and w[i+3]=="~" and w[i+4] in VAR and w[i+5]=="&" and w[i+6]=="|":
      st.append(st.pop()+st.pop()+"^")
      i+=7
    elif w[i]=="~" and i<len(w)-6 and w[i+1]=="&" and w[i+2] in VAR and w[i+3] in VAR and w[i+4]=="~" and w[i+5]=="&" and w[i+6]=="|":
      st.append(st.pop()+st.pop()+"^")
      i+=7
    else:
      st.append(w[i])
      i+=1
  j=0
  wyn=""
  while j<len(st):
  	wyn+=st[j]
  	j+=1
  return wyn

def from_onp(w): #zamieniamy z onp z powrotem na zwykłą
  st=[]
  for z in w: #analogicznie jak przy ewaluacji, tylko tutaj na stos odkładamy odpowiednie wyrażenia nie obliczając ich
    if z in VAR: st.append(z)
    elif z=="~": st.append("~"+st.pop())
    elif z=="^":
      a=st.pop()
      b=st.pop()
      st.append(a+"^"+b)
    elif z=="/":
      a=st.pop()
      b=st.pop()
      st.append(b+"/"+a)
    elif z=="|":
      a=st.pop()
      b=st.pop()
      st.append(b+"|"+a)
    elif z=="&":
      a=st.pop()
      b=st.pop()
      st.append(b+"&"+a)
    elif z==">":
      a=st.pop()
      b=st.pop()
      st.append(b+">"+a)
  wyn=""
  i=0
  while i<len(st):
    wyn+=st[i]
    i+=1
  return wyn

def nawias(w): #składniki wyniku będącego alternatywą koniunkcji umieszczamy w nawiasach
  wyn="("
  i=0
  d=len(w)
  while i<d:
    if w[i]=="|": wyn+=")|("
    else: wyn+=w[i]
    i+=1
  wyn+=")"
  return wyn

def program(w):
  if not spr(w): return "ERROR"
  w=remove_negation_space(w)
  v=var(w)
  w=onp(w)

  dane=set()
  t=True #sprawdzamy, czy przypadkiem wyrażenie nie jest zawsze prawdziwe albo zawsze fałszywe
  f=True
  for x in gen(len(v)):
    if value(w,x)==1:
      f=False
      dane.add(x) #tworzymy zbiór z ciągami wartości zmiennych, dla których wyrażenie wynosi 1 - wejście dla quina
    else: t=False

  if t: return "T"
  if f: return "F"

  dane2=list(reduce(dane))
  dane=list(dane)
  w=wypisz(reduce2(dane,dane2,len(dane),len(dane2))) #redukcja algorytmem quina
  w=imp_dys(xory(onp(w))) #implikacje, dysjunkcje, xory
  w=nawias(from_onp(w)) #dodanie nawiasów
  while w[0]=="(" and w[-1]==")" and spr(w[1:-1]): #usuwanie zbędnych nawiasów
    w=w[1:-1]
  return w

w=input()
print(program(w))