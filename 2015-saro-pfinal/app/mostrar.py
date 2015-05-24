from xml.dom import minidom
from django.views.decorators.csrf import csrf_exempt
import xml.etree.cElementTree as etree
import itertools
import urllib
import sys
from app.models               import Tipos, Usuarios


reload(sys)
sys.setdefaultencoding("utf-8")


def actualizarBBDD(page):
	
	lista = []
	LISTA = []
	contador = 1 
	precio = "0"

	xmldoc = minidom.parse(urllib.urlopen(page))

	itemlist = xmldoc.getElementsByTagName('atributo')

	for element in itemlist:	
				
			if element.getAttribute('nombre') == "TITULO":
				lista= []
				titulo = element.firstChild.nodeValue
				print "titulo " + titulo
				lista.append(titulo)
		
			if element.getAttribute('nombre') == "GRATUITO":
				gratuito = element.firstChild.nodeValue
				if gratuito == "1" :
					gratuito = "Gratuito"
				else:
					gratuito = "Pago"
				print "gratuito " + gratuito
				lista.append(gratuito)
		
			if element.getAttribute('nombre') == "EVENTO-LARGA-DURACION":
				duracion = element.firstChild.nodeValue
				print "duracion " + duracion
				if duracion == "1" :
					duracion = "Larga"
				else:
					duracion = "Corta"
				lista.append(duracion)

			if element.getAttribute('nombre') == "PRECIO":
				precio = element.firstChild.nodeValue
				print "precio " + precio
				lista.append(precio)


			if element.getAttribute('nombre') == "FECHA-EVENTO":
				fecha = element.firstChild.nodeValue
				print "fecha " + fecha
				lista.append(fecha)


			if element.getAttribute('nombre') == "FECHA-FIN-EVENTO":
				fechafin = element.firstChild.nodeValue
				print "fechafin " + fechafin
				lista.append(fechafin)

			if element.getAttribute('nombre') == "CONTENT-URL":
				url = element.firstChild.nodeValue
				print "url " + url
				lista.append(url)

			if element.getAttribute('nombre') == "TIPO":
				tipo = element.firstChild.nodeValue
				print "tipo " + tipo
				lista.append(tipo)
				lista.append(contador)
				contador = contador + 1

				Tipos(titulo = titulo, gratuito = gratuito, fecha = fecha, fechafin = fechafin, url = url, tipo = tipo, precio= precio, duracion= duracion).save()
				precio = "0"
	 			


def mostrarobjeto(DB):
	
	LISTA = []
	lista = []
	
	for objeto in DB:
		lista.append(objeto.titulo)
		lista.append(objeto.gratuito)
		lista.append(objeto.fecha)
		lista.append(objeto.fechafin)
		lista.append(objeto.url)
		lista.append(objeto.tipo)
		lista.append(objeto.id)
		LISTA.append(lista)
		lista = []
	return LISTA
	
	
	
	
	
	
	
	
