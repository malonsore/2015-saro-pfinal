from django.shortcuts             import render
from django.http                  import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from app.models               import Tipos, Usuarios, Usuarios_tipos
from django.shortcuts             import redirect 
from django.contrib.auth          import authenticate, login, logout
from django.contrib.auth.models   import User
from django.template              import Template , Context
from django.template.loader       import get_template
from django.shortcuts             import render_to_response
from datetime                     import date
from app.mostrar              import  mostrarobjeto, actualizarBBDD
import xml.etree.cElementTree as etree
import itertools
import urllib
import sys
from xml.dom import minidom
from BeautifulSoup import BeautifulSoup
import requests
from Final.settings import PROJECT_ROOT
reload(sys)
sys.setdefaultencoding("utf-8")

nombre       = ''
nombreglobal = ''
index = 0

@csrf_exempt
def login_view(request):
	
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username = username, password = password)
		print str(username)
		print str(password)
		if user:
			if user.is_active:
				login(request, user)
				global nombre
				nombre = username
				global nombreglobal
				nombreglobal = username
				direccion = (('/') + str(username))
				return HttpResponseRedirect(direccion)
	
@csrf_exempt			
def logout_view(request):
	logout(request)
	global nombreglobal
	nombreglobal = ''
	
	return HttpResponseRedirect('/')

@csrf_exempt
def indice(request):
	
	page="http://datos.madrid.es/portal/site/egob/menuitem.ac61933d6ee3c31cae77ae7784f1a5a0/?vgnextoid=00149033f2201410VgnVCM100000171f5a0aRCRD&format=xml&file=0&filename=206974-0-agenda-eventos-culturales-100&mgmtid=6c0b6d01df986410VgnVCM2000000c205a0aRCRD"
	
	#######################################################################################################################
	#MOSTRAR PAGINAS PERSONALES
	DB = Usuarios.objects.all()
	
	listaUsu = []
	listaTit = []
	listaDes = []
	listaID  = []
	
	for objeto in DB:
		listaUsu.append(objeto.usuario)
		listaTit.append(objeto.titulo)
		listaDes.append(objeto.descripcion)
		listaID.append(objeto.id)
		
	print str(listaUsu)
	############################################################################################################################

	objeto = Tipos.objects.all().filter(fecha__gte = date.today()).order_by('fecha')
	LISTA = objeto[:10]

	print PROJECT_ROOT
	fichero  = open( PROJECT_ROOT + '/2015-saro-pfinal/templates/index.html')
	template = Template(fichero.read())
	
	print "nombreglobal:" + nombreglobal  

	if nombreglobal == '' :
		value = 0
	else:
		value = 1

	html = template.render(Context({'LISTA1' : listaUsu, 
									'LISTA2' : listaTit,
								    'LISTA3' : listaDes, 
								    'LISTA4' : listaID,
								    'FILA'   : LISTA,
								    'TOPE'   : '8',
								    'VALUE'   : value,
								    'NOMBRE' : nombreglobal}))
	
	return HttpResponse(html)


@csrf_exempt						
def usuario(request, nombre):
	
	print 'USUARIO'
	print nombre

	try:
		usu = Usuarios.objects.get(usuario = nombre)
	except Usuarios.DoesNotExist:
		usu = None

	if usu == None :
		Usuarios(usuario = nombre, descripcion = "descripcion innicial", titulo = "Pagina de usuario :" + nombre).save()
		usu = Usuarios.objects.get(usuario = nombre)

	descripcion = usu.descripcion
	titulo      = usu.titulo
	global index

	if request.method == 'POST': #PARA CAMBIAR TITULO, DESCRIPCION, FONDO...
		
		diccionario = request.POST
		lista       = list(diccionario.keys())
			
		name = str(lista[0])
		valor = request.POST[name]
		
		print 'name:  ' + name
		print 'valor: ' + valor
		
		if name == 'titulo':
			usu.titulo = (valor)
			usu.save()
			titulo = valor
			
		if name == 'descripcion':
			usu.descripcion = (valor)
			usu.save()
			descripcion = valor
		
		if name == 'background':
			usu.background = (valor)
			usu.save()
			background = valor
		
		if name == 'fuente':
			usu.fuente = (valor)
			usu.save()
			fuente = valor
			
		if name == 'letra':
			usu.letra = (valor)
			usu.save()
			letra = valor

		if name == 'siguientes':
			index = index + 1
		if name == 'anteriores':
			index = index - 1
			
	fichero  = open(PROJECT_ROOT + '/2015-saro-pfinal/templates/usuario.html')
	template = Template(fichero.read())
	fichero.close()
	
	usu    = Usuarios.objects.get(usuario = nombre)
	objeto   = usu.incidencias.all()

	print "objeto" + str(len(objeto))
	
	LISTA  = mostrarobjeto(objeto)

	LISTAFECHAS = []
	print "nombre e id :" + nombre + str(usu.id)
	fechas   = Usuarios_tipos.objects.all().filter(usuario = usu.id)
	print "fechas" + str(len(fechas))

	i = 0 
	for elemen in LISTA:
		print "fechaaaa" + fechas[i].elegidaen
		elemen.append(fechas[i].elegidaen)
		i = i +1

	print "index :" + str(index)
	print "finindex" + str((index - 1 )*10)

	LISTA = LISTA[(index * 10):((index + 1 )*10)]


	if nombreglobal == "":
		value = 1
	elif nombreglobal == nombre :
		value = 0
	else:
		value = 2
	
	html = template.render(Context({'USUARIO'         : nombreglobal,
										'VALUE'       : value,
										'FILA'        : LISTA,
										'TOPE'        : '10', 
										'DESCRIPCION' : descripcion, 
										'TITULO'      : titulo,
										'NOMBRE'      : nombre
										}))
	return HttpResponse(html)

@csrf_exempt
def eventos(request):
	
	filtrar = 0 
	fichero  = open(PROJECT_ROOT + '/2015-saro-pfinal/templates/eventos.html')
	template = Template(fichero.read())
	page="http://datos.madrid.es/portal/site/egob/menuitem.ac61933d6ee3c31cae77ae7784f1a5a0/?vgnextoid=00149033f2201410VgnVCM100000171f5a0aRCRD&format=xml&file=0&filename=206974-0-agenda-eventos-culturales-100&mgmtid=6c0b6d01df986410VgnVCM2000000c205a0aRCRD"

	LISTA = []
	if request.method == 'POST':
		diccionario = request.POST
		lista       = list(diccionario.keys())
		
		DB = Tipos.objects.all()
		
		if len(lista) != 0:
			
			columna = str(lista[0])
			print 'NAME: ' + nombreglobal
			filtrado = request.POST[columna]
			valor = str(filtrado)

			if columna == 'seguir':
				
				EVENTO = Tipos.objects.get(id = valor)				
				global nombre
				usu = Usuarios.objects.get(usuario = nombreglobal)
				usu.incidencias.add(EVENTO)
				usu.save()
				Usuarios_tipos(usuario = usu.id, tipo = valor, elegidaen = date.today() ).save()
			elif columna == 'actualizar':
				Tipos.objects.all().delete()
				actualizarBBDD(page)
			else:
				filtrar = 1
######################################################################################################################
	
	objeto = Tipos.objects.all().filter(fecha__gte = date.today()).order_by('fecha')
	LISTA = objeto
	HORA  = date.today()
	if filtrar == 1:
		if columna == "gratuito":
			objeto = Tipos.objects.all().filter(gratuito = valor).order_by('fecha')
			LISTA = objeto
		if columna == "duracion":
			objeto = Tipos.objects.all().filter(duracion = valor).order_by('fecha')
			LISTA = objeto
		if columna == "titulo":
			objeto = Tipos.objects.all().filter(titulo = valor).order_by('fecha')
			LISTA = objeto
		if columna == "fecha":
			objeto = Tipos.objects.all().filter(fecha = valor).order_by('fecha')
			LISTA = objeto
		if columna == "precio":
			objeto = Tipos.objects.all().filter(precio = valor).order_by('fecha')
			LISTA = objeto	
		filtrar = 0
		
	print "nombre golbal" + nombreglobal

	if nombreglobal == '' :
		value = 0
	else:
		value = 1

	html = template.render(Context({'TOPE'   : '10',
									'FILA'   : LISTA,
									'NOMBRE' : nombreglobal,
									'HORA'   : HORA,
									'VALUE'   : value}))
	return HttpResponse(html)

@csrf_exempt
def canalRSS (request, canal):
	print 'canalRSS'
	print 'CANAL RSS DE: ' + (canal)
	
	fichero  = open(PROJECT_ROOT + '/2015-saro-pfinal/templates/eventos.xml')
	template = Template(fichero.read())
	fichero.close()
	
	usuCanal = canal
	usu      = Usuarios.objects.get(usuario = usuCanal)
	objeto   = usu.incidencias.all()
	
	LISTA = []
	lista = []
	
	LISTA  = mostrarobjeto(objeto)
	
	FECHA = date.today()
	
	xml = template.render(Context({'LISTA' : LISTA,
								   'FECHA' : FECHA}))
	
	return HttpResponse(xml)


@csrf_exempt
def ayuda (request):
	
	
	fichero  = open(PROJECT_ROOT + '/2015-saro-pfinal/templates/ayuda.html')
	
	return HttpResponse(fichero)


@csrf_exempt
def css(request):

	if nombreglobal == '':
		fondo = ""
		color = "black"
		tamano = "medium"
	else:

		usu = Usuarios.objects.get(usuario = nombre)

		print "usu.background " + usu.background
		fondo = getColor(usu.background)
		color = getColor(usu.letra)
		tamano = getTamano(usu.fuente)

	fichero  = open(PROJECT_ROOT + '/2015-saro-pfinal/templates/css/estilos.css')
	template = Template(fichero.read())

	css = template.render(Context({'FONDO' : fondo, 
									'COLOR' : color,
									'TAMANO' : tamano}))
	response = HttpResponse(css)
	response['Content-Type'] = 'text/css'
	return response

@csrf_exempt
def image(request):

	fichero  = open(PROJECT_ROOT + '/2015-saro-pfinal/templates/img/madrid.jpeg')
	response = HttpResponse(fichero)
	response['Content-Type'] = 'image/jpeg'
	return response

@csrf_exempt
def portales(request, page):

	print page
	print request.GET['vgnextfmt'] 
	print request.GET['vgnextoid'] 
	print request.GET['vgnextchannel'] 

	return HttpResponseRedirect('http://www.madrid.es/portales/' + page + "?vgnextfmt=" + request.GET['vgnextfmt'] + "&" +
																			"vgnextoid=" + request.GET['vgnextoid'] + "&" +
																			 "vgnextchannel=" + request.GET['vgnextchannel'])



@csrf_exempt						
def actividad(request, id):
	
	page="http://datos.madrid.es/portal/site/egob/menuitem.ac61933d6ee3c31cae77ae7784f1a5a0/?vgnextoid=00149033f2201410VgnVCM100000171f5a0aRCRD&format=xml&file=0&filename=206974-0-agenda-eventos-culturales-100&mgmtid=6c0b6d01df986410VgnVCM2000000c205a0aRCRD"
	
	#######################################################################################################################
	#MOSTRAR PAGINAS PERSONALES
	DB = Usuarios.objects.all()
	
	listaUsu = []
	listaTit = []
	listaDes = []
	listaID  = []
	
	for objeto in DB:
		listaUsu.append(objeto.usuario)
		listaTit.append(objeto.titulo)
		listaDes.append(objeto.descripcion)
		listaID.append(objeto.id)
		
	print str(listaUsu)
	############################################################################################################################

	objeto = Tipos.objects.all().filter(id = id)
	LISTA = objeto

	fichero  = open(PROJECT_ROOT + '/2015-saro-pfinal/templates/actividad.html')
	template = Template(fichero.read())
	
	print "nombreglobal:" + nombreglobal  

	if nombreglobal == '' :
		value = 0
	else:
		value = 1

	r = requests.get(objeto[0].url)
	soup = BeautifulSoup(r.text)

	mydivs = soup.findAll("div", { "class" : "listadoInfo" })
	info = ""
	for link in mydivs:
		info = str(link)

	html = template.render(Context({'LISTA1' : listaUsu, 
									'LISTA2' : listaTit,
								    'LISTA3' : listaDes, 
								    'LISTA4' : listaID,
								    'FILA'   : LISTA,
								    'TOPE'   : '8',
								    'VALUE'   : value,
								    'NOMBRE' : nombreglobal,
								    'INFO' : info}))
	
	return HttpResponse(html)

def getColor(idColor):

	print "idcolor " + idColor
	COLOR = ""
	if idColor == "2":
		COLOR = "red"
	elif idColor == "1":
		COLOR = "green"
	elif idColor == "3":
		COLOR = "blue"
	return COLOR

def getTamano(idColor):

	COLOR = ""
	if idColor == "2":
		COLOR = "medium"
	elif idColor == "1":
		COLOR = "small"
	elif idColor == "3":
		COLOR = "large"
	return COLOR
