from socket import *
import time
from xml.dom import minidom

buf=[]

def get_meteo():
	s=socket(AF_INET,SOCK_STREAM)
	s.connect(("meteo.ftj.agh.edu.pl",80))
	s.send(b"GET /meteo/meteo.xml\n")
	r=s.recv(1024).decode()
	s.close()
	return r

def parse_xml(dane):
	t={}
	xmldoc=minidom.parseString(dane)
	meteo=xmldoc.getElementsByTagName("meteo")[0]
	for d in meteo.childNodes:
		for c in d.childNodes:
			if c.nodeType==minidom.Node.ELEMENT_NODE:
				t[c.nodeName]=c.childNodes[0].nodeValue
	return t

def sr(f):
	buf
	def nowa():
		x=f()
		buf.append(x)
		if len(buf)>5: buf.pop(0)
		s=0.0
		for el in buf: s+=el
		s/=len(buf)
		return s
	return nowa

@sr
def get_tmp():
	return float(parse_xml(get_meteo())["ta"][:-3])

for i in range(10):
	x=get_tmp()
	f=open("dane","a")
	f.write("{}\n".format(x))
	f.close()
	time.sleep(5)