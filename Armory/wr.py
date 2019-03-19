from urllib.request import *
from bs4 import BeautifulSoup
from random import randint
from tkinter import *

def connect(urls,n):
    response=urlopen(urls[n])
    data=response.read()
    soup=BeautifulSoup(data,'html.parser')
    data=soup.get_text()
    return data

def parse2(data):
    i=0
    s=0
    can=False
    can2=False
    stop=False
    l=[]
    offset=0

    for line in data.splitlines():
        if line=="Country": can=True
        if line=="See also[edit]": break
        if can:
            s+=1
            if s==8: can2=True

        if can and can2:
            if i==15:
                i=0
                if offset==999: offset=8
                if offset==99: offset=10
                if offset==9999: offset=3
                if offset==55: offset=10
            if i==0+offset and line!="" and not stop: l.append(line)
            if line=="Beretta Mx4 Storm": offset+=2
            if line=="H&K UMP[2]": offset+=3
            if line=="Heckler & Koch MP5": offset=999
            if line=="Heckler & Koch MP7": offset=99
            if line=="KRISS Vector":
                offset=1
                stop=True
            if line=="Labora Fontbernat M-1938":
                l.append(line)
                stop=False
            if line=="Steyr AUG PARA": offset=9999
            if line=="Uzi": offset=55
            i+=1
    return l

def semi(data):
    can=False
    l=[]

    for line in data.splitlines():
        if line=="See also[edit]": break
        if line=="AAC Honey Badger PDW": can=True
        if line==" Mauser M1916": l.append("Mauser M1916")
        if can==True and line!=" Mauser M1916": l.append(line)

    l.pop()
    return l

def parse(data,n):
    i=0
    s=0
    can=False
    can2=False
    l=[]
    offset=0
    if n!=0 and n!=1: offset=2

    for line in data.splitlines():
        if (line=="Years" and n==0) or (line=="Country" and n!=0): can=True
        if line=="See also[edit]": break
        if can:
            s+=1
            if (s==4 and n!=1) or (s==6 and n==1): can2=True

        if can and can2:
            if i==13:
                i=0
                if offset==99 or offset==999: offset=4
            if i==0+offset and line!="": l.append(line)
            if line=="FB MSBS": i=-3
            if line=="Astra A-60": offset+=2
            if line=="Browning BSS": offset=99
            if line=="Smith & Wesson Model 386": offset=999
            i+=1
    return l

def rand(n,l):
    res=[]
    for i in range(n):
        r=randint(0,len(l)-1)
        res.append(l[r])
        del l[r]
    return res

url1="https://en.wikipedia.org/wiki/List_of_assault_rifles"
url2="https://en.wikipedia.org/wiki/List_of_carbines"
url3="https://en.wikipedia.org/wiki/List_of_pistols"
url4="https://en.wikipedia.org/wiki/List_of_battle_rifles"
url5="https://en.wikipedia.org/wiki/List_of_machine_guns"
url6="https://en.wikipedia.org/wiki/List_of_submachine_guns"
url7="https://en.wikipedia.org/wiki/List_of_shotguns"
url8="https://en.wikipedia.org/wiki/List_of_semi-automatic_rifles"
url9="https://en.wikipedia.org/wiki/List_of_sniper_rifles"
url10="https://en.wikipedia.org/wiki/List_of_revolvers"
url11="https://en.wikipedia.org/wiki/List_of_rifles"
urls=[url1,url2,url3,url4,url5,url6,url7,url8,url9,url10,url11]

window=Tk()

def output(x,c,r):
    data=connect(x,c.get())
    if c.get()!=5: l=parse(data,c.get())
    elif c.get()!=7: l=parse2(data)

    if c.get()==7:
        l=semi(data)
        data=connect(x,10)
        l+=parse(data,c.get())
    l=list(set(l))
    res=rand(r.get(),l)

    i=0
    global w2
    w2.delete(0,END)
    for e in res:
        w2.insert(i,e)
        i+=1

window.title("Weapon randomizer")
window.geometry('830x512')
lbl=Label(window,text="Select weapon category:",font=(50))
lbl.grid(column=0,row=0,sticky='w')

lbl2=Label(window,text="Choose the number of weapons you wish to acquire:",font=(50))
lbl2.grid(column=0,row=11,pady=(20,0),sticky='w')
var=IntVar()
var.set(0)
vs=list(range(1,31))
spin=Spinbox(window,values=vs,width=5,textvariable=var,state="readonly")
spin.grid(column=0,row=12,sticky='w')

selected=IntVar()
r1=Radiobutton(window,text="Assault rifles",font=(20),value=0,variable=selected)
r2=Radiobutton(window,text="Carbines",font=(20),value=1,variable=selected)
r3=Radiobutton(window,text="Pistols",font=(20),value=2,variable=selected)
r4=Radiobutton(window,text="Battle rifles",font=(20),value=3,variable=selected)
r5=Radiobutton(window,text="Machine guns",font=(20),value=4,variable=selected)
r6=Radiobutton(window,text="Submachine guns",font=(20),value=5,variable=selected)
r7=Radiobutton(window,text="Shotguns",font=(20),value=6,variable=selected)
r8=Radiobutton(window,text="Rifles",font=(20),value=7,variable=selected)
r9=Radiobutton(window,text="Sniper rifles",font=(20),value=8,variable=selected)
r10=Radiobutton(window,text="Revolvers",font=(20),value=9,variable=selected)

r1.grid(column=0,row=1,sticky='w')
r2.grid(column=0,row=2,sticky='w')
r3.grid(column=0,row=3,sticky='w')
r4.grid(column=0,row=4,sticky='w')
r5.grid(column=0,row=5,sticky='w')
r6.grid(column=0,row=6,sticky='w')
r7.grid(column=0,row=7,sticky='w')
r8.grid(column=0,row=8,sticky='w')
r9.grid(column=0,row=9,sticky='w')
r10.grid(column=0,row=10,sticky='w')

w=Label(window,text="Generated weapons:",font=(50))
w.grid(column=1,row=0,padx=10,sticky='w')

w2=Listbox(window,width=37,height=24,font=(20))
w2.grid(column=1,row=1,rowspan=20,padx=(10,0),sticky='ns')
sc=Scrollbar(window,width=15)
sc.grid(column=3,row=1,rowspan=20,sticky='ns')
w2.config(yscrollcommand=sc.set)
sc.config(command=w2.yview)

btn=Button(window,text="Generate weapons",command=lambda *args: output(urls,selected,var))
btn.grid(column=0,row=13,sticky='w')
window.mainloop()
