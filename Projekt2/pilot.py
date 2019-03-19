from socket import *
import yaml
from tkinter import *
from tkinter import ttk

def parse_yaml(dane):
	name=""
	rooms=[]
	for e in dane:
		for key,value in e.items():
			if value==None: name=key #e jest słownikiem z nazwą i urządzeniami, nazwa pokoju ma przypisane None
		del e[name] #usunięcie nazwy zabezpiecza przed duplikacją danych na liście wynikowej
		rooms.append([name,e.items()]) #jeden element nowej listy to nazwa i lista urządzeń z danego pokoju
	for r in rooms: print(r[1])
	return rooms

def GUI(e):
	def on2(e):
		def f(x=e):
			s=socket(AF_INET,SOCK_DGRAM)
			s.setsockopt(SOL_SOCKET,SO_BROADCAST,1) #ustawiwamy możliwość wysłania na adres broadcastowy
			b="255.255.255.255"
			port=2018
			m='on '+e[0] #e to element w którym jest nazwa urządzenia i identyfikator
			m2=str.encode(m) #zamieniamy str na bytes, bo inaczej nie da się wysłać
			s.sendto(m2,(b,port))
		return f

	def off2(e): #analogicznie jak on2(e)
		def f(x=e):
			s=socket(AF_INET,SOCK_DGRAM)
			s.setsockopt(SOL_SOCKET,SO_BROADCAST,1)
			b="255.255.255.255"
			port=2018
			m='off '+e[0]
			m2=str.encode(m)
			s.sendto(m2,(b,port))
		return f

	window=Tk() #tworzymy okno korzystając z funkcji biblioteki tkinter
	window.title("WP")
	window.geometry('300x400')
	tab=ttk.Notebook(window) #zakładki okna programu

	for r in rooms:
		t=ttk.Frame(tab)
		tab.add(t,text=r[0]) #na zakładce jest umieszczona nazwa pokoju
		i=0
		for e in r[1]: #lista urządzeń przypisana do pokoju
			l=Label(t,text=e[1])
			l.grid(row=i,sticky=W) #wyrównanie do lewej, i jako licznik rzędów, żeby każde urządzenie wypisać w nowym
			on=Button(t,text="On",command=on2(e)) #przycisk, funkcja obsługi to funkcja zwrócona przez on2(e)
			on.grid(column=1,row=i)
			off=Button(t,text="Off",command=off2(e))
			off.grid(column=2,row=i)
			i=i+1

	tab.pack(expand=1,fill='both') # okno zakładki wypełnia całość okna programu
	window.mainloop() #pętla utrzymująca okno

f=input("Enter YAML configuration file name: ")
with open(f) as config:
    try:
        dane=yaml.load(config) #wczytujemy dane z pliku YAML uważając na YAMLError
    except yaml.YAMLError as e:
        print(e)

rooms=parse_yaml(dane)
GUI(rooms) #parsujemy wczytane dane i odpalamy okno programu