import yaml
from tkinter import *
from tkinter.ttk import *

categories=[]
value=[]

def parse_yaml(dane):
	name=""
	for e in dane:
		for key,value in e.items():
			if value==None: name=key
		del e[name]
		categories.append([name,e.items()])

def category_select(event):
	for e in value:
		if all_categories.get()==e: chosen_category.set(e)
	for g in weapons:
		if chosen_category.get()==g[0]: chosen_guns=g

def gun_select(event):
	for e in chosen_guns:
		if all_guns.get()==e.get(): chosen_gun.set(e)

with open("weapons.yaml") as config:
    try:
        dane=yaml.load(config)
    except yaml.YAMLError as e:
        print(e)

parse_yaml(dane)

window=Tk()
chosen_category=StringVar()
chosen_gun=StringVar()
chosen_guns=[]
weapons=[]
window.title("Ammunition Manager")
window.geometry('500x400')
category_tmp=""

i=0
for e in categories:
	if e[0]!=category_tmp:
		category_tmp=e[0]
		value.append(e[0])
		weapons.append([])
		weapons[i].append(e[0])
		for g in e[1]: weapons[i].append(g[1])
		i+=1

all_categories=Combobox(window,state="readonly",values=value)
l=Label(window,text="Weapon category: ")
l.grid(column=0,row=2)
all_categories.grid(column=10,row=2)
all_categories.bind("<<ComboboxSelected>>",category_select)

all_guns=Combobox(window,state="readonly",values=chosen_guns)
l=Label(window,text="Weapon: ")
l.grid(column=0,row=3)
all_guns.grid(column=6,row=3)
all_guns.bind("<<ComboboxSelected>>",gun_select)

t=Label(window,textvariable=chosen_gun)
t.grid(column=0,row=5)
t2=Label(window,textvariable=chosen_category)
t2.grid(column=0,row=6)
window.mainloop()
