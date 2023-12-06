from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import date 
from django.contrib import auth

# Create your models here.
class FamiliaProfesional(models.Model):
	name = models.CharField(max_length=60, null=True)
	@property
	def partidos(self):
		return Curso.objects.filter(familia_profesional=self)
	def __str__(self):
		return f"{self.name}"




class Provincia(models.Model):
	name = models.CharField(max_length=60, null=True)
	@property
	def partidos(self):
		return Partido.objects.filter(provincia=self)
	def __str__(self):
		return f"{self.name}"




class Partido(models.Model):
	name = models.CharField(max_length=60, null=True)
	provincia = models.ForeignKey(Provincia, on_delete=models.CASCADE, null=False, related_name="partidos")
	def __str__(self):
		return f"{self.name}"




class Institucion(models.Model):
	name = models.CharField(max_length=60, null=True)
	partido =  models.ForeignKey(Partido, on_delete=models.SET_NULL, null=True, related_name="instituciones")
	cue =  models.CharField(max_length=12, null=True)
	# cursos = models.ForeignKey(Curso, on_delete=models.SET_NULL, null=True, related_name="instituciones")
	@property
	def cursos(self):
		return Curso.objects.filter(institucion=self)
	def __str__(self):
		return f"{self.name}"
	def get_absolute_url(self):
		return reverse('aplicacion:centros-detail', args=[self.pk])




class Curso(models.Model):
	name = models.CharField(max_length=60, null=True)
	descripcion = models.TextField(blank=True, max_length=5000, null=True)
	familia_profesional = models.ForeignKey(FamiliaProfesional, on_delete=models.CASCADE, null=True)
	institucion = models.ForeignKey(Institucion, on_delete=models.CASCADE, null=True)
	slug = models.SlugField(default="", null=True)
	
	estudiantes = models.ManyToManyField("Estudiante", blank=True)
		
	def generate_slug_new(self):
		return slugify(f"{self.name} {self.institucion} {self.pk}")
		
	def save(self, *args, **kwargs):
		super().save(*args, **kwargs)
		self.slug = self.generate_slug_new()
		super().save(*args, **kwargs)

	def __str__(self):
		# return f"{self.name} ({self.familia_profesional.name})"
		return f"{self.name}"
		
	@property
	def related_estudiantes(self):
		# return Estudiante.objects.filter(curso=self)
		return self.estudiantes.all()




class Estudiante(models.Model, LoginRequiredMixin):
	name = models.CharField(max_length=255, null=True)
	lastname = models.CharField(max_length=255, null=True)
	nacimiento = models.DateField(null=True)
	email = models.EmailField(null=True)
	phone = models.CharField(max_length=20, null=True)
	slug = models.SlugField(default="", null=True)
	updated = models.DateTimeField(auto_now=True)
	created = models.DateTimeField(auto_now_add=True)
	# escuela = models.ForeignKey(Escuela, on_delete=models.CASCADE, null=True, related_name="estudiantes")
	# curso = models.ForeignKey(Curso, on_delete=models.SET_NULL, null=True, related_name="estudiantes")
	
	cursos = models.ManyToManyField("Curso", blank=True)
		
	def generate_slug_new(self):
		return slugify(f"{self.name} {self.lastname} {self.pk}")
		
	def save(self, *args, **kwargs):
		super().save(*args, **kwargs)
		self.slug = self.generate_slug_new()
		super().save(*args, **kwargs)
		
	def __str__(self):
		return f"{self.name} {self.lastname}"
		
	@property
	def age(self):
		return date.today().year - self.nacimiento.year
		
	@property
	def related_cursos(self):
		return self.cursos.all()
	
	#coopado
	class Meta:
		ordering = ["-updated", '-created']
		
		


class Usuario(auth.models.User):
	avatar = models.ImageField(upload_to="media/avatares", null=True, blank=True)
	# avatar = models.ForeignKey("Avatar", on_delete=models.SET_NULL)
	# @property
	# def related_avatar(self):
		# return Avatar.objects.get(usuario=self)
		
		


class AvatarPDF(models.Model):
	usuario = models.ForeignKey(auth.models.User, on_delete=models.CASCADE)
	imagen = models.ImageField(upload_to="media/avataresPDF", null=True, blank=True)
		
	def __str__(self):
		return f"Avatar 00{self.id} | {self.usuario} | url: {self.imagen.url}"
		
		
	
class Queja(models.Model):
	nombre = models.CharField(max_length=70, null=True)
	dni = models.IntegerField(null=True)
	email = models.EmailField(null=True)
	mensaje = models.TextField(max_length=512, null=True)
	atendido = models.BooleanField(default=False, null=True)
		
	def __str__(self):
		return f"Atendido:{self.atendido}|{self.id}|{self.nombre}|{self.mensaje[:33]}..."
		
		

# Estudiante.objects.all() 				#para pasar como referencia al template
# Curso.objects.all()


# Estudiante.objects.all().values()		#los muestra
# Curso.objects.all().values()