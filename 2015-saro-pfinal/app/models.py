from django.contrib.auth.models   import User
from django.db                    import models

class Tipos(models.Model):
	titulo       = models.CharField(max_length = 500)
	gratuito  = models.CharField(max_length = 500)
	fecha  = models.CharField(max_length = 500)
	fechafin  = models.CharField(max_length = 500)
	url      = models.CharField(max_length = 500)
	tipo  = models.CharField(max_length = 500)
	duracion  = models.CharField(max_length = 500)
	precio  = models.CharField(max_length = 500)

	#comentario = models.CharField(max_length = 500)
	#puntuacion = models.CharField(max_length = 500)

class Usuarios(models.Model):
	usuario     = models.CharField(max_length = 200)
	titulo      = models.CharField(max_length = 200)
	descripcion = models.CharField(max_length = 200)
	incidencias = models.ManyToManyField(Tipos)
	amigos      = models.ManyToManyField(User)
	background  = models.CharField(max_length = 200)
	fuente      = models.CharField(max_length = 200)
	letra       = models.CharField(max_length = 200)

class Usuarios_tipos(models.Model):
	usuario     = models.CharField(max_length = 200)
	tipo        = models.CharField(max_length = 200)
	elegidaen    = models.CharField(max_length = 200)
	
	
