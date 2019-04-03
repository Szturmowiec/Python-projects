import json
from tkinter import *
from tkinter.ttk import Combobox

class objectview(object):
    def __init__(self,d):
        self.__dict__=d

class Gun:
    def __init__(name,range,accuracy,cqb,long):
        self.name=name
        self.range=range
        self.accuracy=accuracy
        self.cqb=cqb
        self.long=long

class Scope:
    def __init__(name,short,mid,long,range):
        self.name=name
        self.short=short
        self.mid=mid
        self.long=long
        self.range=range

class Attachement:
    def __init__(name,short,mid,long):
        self.name=name
        self.short=short
        self.mid=mid
        self.long=long

def read_guns():
    data=[]
    guns=[]
    with open("assault.json") as file:
        data=json.load(file)
    with open("pm.json") as file:
        data+=json.load(file)

    for e in data: guns.append(objectview(e))
    names=[]
    for e in guns: names.append(e.name)

    optics=[]
    with open("optics.json") as file:
        data=json.load(file)
    for e in data: optics.append(objectview(e))

    attachements=[]
    with open("attachements.json") as file:
        data=json.load(file)
    for e in data: attachements.append(objectview(e))

    return guns,names,optics,attachements

(guns,names,optics,attachements)=read_guns()
window=Tk()
chosen_gun=StringVar()
scope=IntVar()
skill=BooleanVar()
cover=IntVar()
morale=IntVar()
pos=IntVar()
aim=IntVar()
fog=BooleanVar()
bushes=BooleanVar()
night=BooleanVar()
drunk=BooleanVar()
move=BooleanVar()
grip=BooleanVar()
bipod=BooleanVar()
barrel=BooleanVar()
night_vision=BooleanVar()
butt=BooleanVar()
result=StringVar()
result.set("11")

def gun_select(event):
    for e in names:
        if weapon.get()==e: chosen_gun.set(e)

def calculate(chosen_gun,scope,skill,cover,morale,pos,aim,fog,bushes,night,drunk,move,grip,bipod,barrel,night_vision,butt,guns,optics,attachements,range,wounds):
    hard=11
    range=int(range)
    wounds=int(wounds)
    gun=None
    for e in guns:
        if e.name==chosen_gun.get(): gun=e
    if range<=20: hard-=gun.cqb
    if range>=150: hard-=gun.long
    hard-=gun.accuracy
    hard+=wounds
    if range>gun.range: hard+=15

    if range<=50: hard+=3
    if range>50 and range<=100: hard+=5
    if range>100 and range<=150: hard+=7
    if range>150 and range<=200: hard+=9
    if range>200 and range<=250: hard+=11
    if range>250 and range<=300: hard+=13
    if range>300 and range<=350: hard+=16
    if range>350 and range<=400: hard+=18
    if range>400 and range<=450: hard+=20
    if range>450 and range<=500: hard+=22
    if range>500 and range<=600: hard+=24
    if range>600 and range<=700: hard+=27
    if range>700 and range<=800: hard+=30
    if range>150 and scope.get()==0:
        tmp=(range-150)/50
        hard+=2*tmp

    if skill.get(): hard-=4
    else: hard+=2
    if cover.get()==1: hard+=2
    if cover.get()==2: hard+=4
    if bushes.get(): hard+=2
    if fog.get(): hard+=3
    if night.get(): hard+=3
    if drunk.get(): hard+=5
    if morale.get()==0: hard+=5
    if morale.get()==2: hard-=2
    if pos.get()==0: hard+=1
    if pos.get()==2: hard-=1
    if move.get(): hard+=5
    hard-=aim.get()

    if bipod.get() and range>=20 and pos.get()==2: hard-=2
    if grip.get(): hard-=1
    if barrel.get(): hard-=1
    if night_vision.get() and range<=150 and night.get(): hard-=3
    if butt.get() and range<=20: hard+=1
    if butt.get() and range>20: hard-=2

    scope_range=0
    if scope.get()==1 and range<=20: hard-=2
    if scope.get()==2:
        scope_range=200
        if range<=20: hard+=3
        if range>20 and range<=150: hard-=2
    if scope.get()==3:
        scope_range=300
        if range<=20: hard+=4
        if range>20 and range<=150: hard-=3
        if range>150: hard-=1
    if scope.get()==4:
        scope_range=400
        if range<=20: hard+=5
        if range>20 and range<=150: hard-=4
        if range>150: hard-=2
    if scope.get()==5:
        scope_range=500
        if range<=20: hard+=7
        if range>20 and range<=150: hard-=4
        if range>150: hard-=3
    if scope.get()==6:
        scope_range=600
        if range<=20: hard+=10
        if range>20 and range<=150: hard-=3
        if range>150: hard-=4
    if scope.get()==7:
        scope_range=800
        if range<=20: hard+=15
        if range>150: hard-=6
    if scope.get()==8:
        scope_range=1000
        if range<=20: hard+=20
        if range>20 and range<=150: hard+=2
        if range>150: hard-=8

    if scope.get()!=0 and range>scope_range:
        tmp=(range-max(150,scope_range))/50
        hard+=2*tmp
    global result
    result.set(str(hard))

window.title("Firefight calculator")
window.geometry("1000x650")
lbl=Label(window,text="Weapon: ",font=(20))
lbl.grid(column=0,row=0,sticky='w')
weapon=Combobox(window,state="readonly",values=names)
weapon.grid(column=1,row=0)
weapon.bind("<<ComboboxSelected>>",gun_select)

lbl2=Label(window,text="Range: ",font=(20))
lbl2.grid(column=0,row=1,sticky='w')
dst=Entry(window,width=10)
dst.insert(END,"0")
dst.grid(column=1,row=1)

lbl3=Label(window,text="Optics: ",font=(20))
lbl3.grid(column=0,row=2,sticky='w')
sc=[]
sc.append(Radiobutton(window,text="None",font=(20),value=0,variable=scope))
sc.append(Radiobutton(window,text="Holo/RDS",font=(20),value=1,variable=scope))
sc.append(Radiobutton(window,text="x2",font=(20),value=2,variable=scope))
sc.append(Radiobutton(window,text="x3",font=(20),value=3,variable=scope))
sc.append(Radiobutton(window,text="x4",font=(20),value=4,variable=scope))
sc.append(Radiobutton(window,text="x6",font=(20),value=5,variable=scope))
sc.append(Radiobutton(window,text="x8",font=(20),value=6,variable=scope))
sc.append(Radiobutton(window,text="x12",font=(20),value=7,variable=scope))
sc.append(Radiobutton(window,text="x16",font=(20),value=8,variable=scope))
for i in range(len(sc)): sc[i].grid(column=0,row=3+i,sticky='w')

lbl4=Label(window,text="Shooting skills: ",font=(20))
lbl4.grid(column=0,row=12,sticky='w')
sk=Checkbutton(window,text='',var=skill)
sk.grid(column=1,row=12,sticky='w')

lbl5=Label(window,text="Cover: ",font=(20))
lbl5.grid(column=0,row=13,sticky='w')
cv=[]
cv.append(Radiobutton(window,text="None",font=(20),value=0,variable=cover))
cv.append(Radiobutton(window,text="Half",font=(20),value=1,variable=cover))
cv.append(Radiobutton(window,text="Full",font=(20),value=2,variable=cover))
for i in range(len(cv)): cv[i].grid(column=0,row=14+i,sticky='w')

lbl6=Label(window,text="Fog: ",font=(20))
lbl6.grid(column=0,row=17,sticky='w')
sk2=Checkbutton(window,text='',var=fog)
sk2.grid(column=1,row=17,sticky='w')

lbl7=Label(window,text="Difficult terrain: ",font=(20))
lbl7.grid(column=0,row=18,sticky='w')
sk3=Checkbutton(window,text='',var=bushes)
sk3.grid(column=1,row=18,sticky='w')

lbl8=Label(window,text="Night: ",font=(20))
lbl8.grid(column=0,row=19,sticky='w')
sk4=Checkbutton(window,text='',var=night)
sk4.grid(column=1,row=19,sticky='w')

lbl9=Label(window,text="Drunk: ",font=(20))
lbl9.grid(column=0,row=20,sticky='w')
sk5=Checkbutton(window,text='',var=drunk)
sk5.grid(column=1,row=20,sticky='w')

lbl10=Label(window,text="Moving target: ",font=(20))
lbl10.grid(column=0,row=21,sticky='w')
sk6=Checkbutton(window,text='',var=move)
sk6.grid(column=1,row=21,sticky='w')

lbl11=Label(window,text="Morale: ",font=(20))
lbl11.grid(column=0,row=22,sticky='w')
m=[]
m.append(Radiobutton(window,text="Low",font=(20),value=0,variable=morale))
m.append(Radiobutton(window,text="Normal",font=(20),value=1,variable=morale))
m.append(Radiobutton(window,text="High",font=(20),value=2,variable=morale))
for i in range(len(m)): m[i].grid(column=0,row=23+i,sticky='w')

lbl12=Label(window,text="Position: ",font=(20))
lbl12.grid(column=2,row=0,sticky='w')
p=[]
p.append(Radiobutton(window,text="Standing",font=(20),value=0,variable=pos))
p.append(Radiobutton(window,text="Crouched",font=(20),value=1,variable=pos))
p.append(Radiobutton(window,text="Prone",font=(20),value=2,variable=pos))
for i in range(len(p)): p[i].grid(column=2,row=1+i,sticky='w')

lbl13=Label(window,text="Turns spent aiming: ",font=(20))
lbl13.grid(column=2,row=4,sticky='w')
a=[]
a.append(Radiobutton(window,text="0",font=(20),value=0,variable=aim))
a.append(Radiobutton(window,text="1",font=(20),value=1,variable=aim))
a.append(Radiobutton(window,text="2",font=(20),value=2,variable=aim))
for i in range(len(a)): a[i].grid(column=2,row=5+i,sticky='w')

lbl14=Label(window,text="Wound penalty: ",font=(20))
lbl14.grid(column=2,row=8,sticky='w')
dst2=Entry(window,width=10)
dst2.insert(END,"0")
dst2.grid(column=3,row=8)

lbl15=Label(window,text="Grip: ",font=(20))
lbl15.grid(column=2,row=9,sticky='w')
sk7=Checkbutton(window,text='',var=grip)
sk7.grid(column=3,row=9,sticky='w')

lbl16=Label(window,text="Bipod: ",font=(20))
lbl16.grid(column=2,row=10,sticky='w')
sk8=Checkbutton(window,text='',var=bipod)
sk8.grid(column=3,row=10,sticky='w')

lbl17=Label(window,text="Barrel extension: ",font=(20))
lbl17.grid(column=2,row=11,sticky='w')
sk9=Checkbutton(window,text='',var=barrel)
sk9.grid(column=3,row=11,sticky='w')

lbl18=Label(window,text="Noctovisor: ",font=(20))
lbl18.grid(column=2,row=12,sticky='w')
sk10=Checkbutton(window,text='',var=night_vision)
sk10.grid(column=3,row=12,sticky='w')

lbl19=Label(window,text="Butt extension: ",font=(20))
lbl19.grid(column=2,row=13,sticky='w')
sk11=Checkbutton(window,text='',var=butt)
sk11.grid(column=3,row=13,sticky='w')

btn=Button(window,text="Calculate shooting difficulty",command=lambda *args: calculate(chosen_gun,scope,skill,cover,morale,pos,aim,fog,bushes,night,drunk,move,grip,bipod,barrel,night_vision,butt,guns,optics,attachements,dst.get(),dst2.get()))
btn.grid(column=2,row=14,sticky='w')

lbl20=Label(window,textvariable=result,font=(20))
lbl20.grid(column=2,row=15,sticky='w')
window.mainloop()
