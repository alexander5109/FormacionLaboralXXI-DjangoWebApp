from django.db import models
from datetime import date 
from django.contrib.auth.models import User


# Create your models here.




class ExamResult(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	
	question_1 = models.BooleanField(null=True)
	question_2 = models.BooleanField(null=True)
	question_3 = models.BooleanField(null=True)
	question_4 = models.BooleanField(null=True)
	
	question_5 = models.IntegerField(null=True)
	question_6 = models.IntegerField(null=True)
	question_7 = models.IntegerField(null=True)
	question_8 = models.IntegerField(null=True)
	question_9 = models.IntegerField(null=True)
	question_10 = models.IntegerField(null=True)
	
	question_11 = models.FileField(null=True)
	

	question_12_s1 = models.BooleanField(null=True)
	question_12_s2 = models.BooleanField(null=True)
	question_12_s3 = models.BooleanField(null=True)
	question_12_s4 = models.BooleanField(null=True)
	question_12_s5 = models.BooleanField(null=True)
	question_12_s6 = models.BooleanField(null=True)
	question_12_s7 = models.BooleanField(null=True)

	question_13_s1 = models.BooleanField(null=True)
	question_13_s2 = models.BooleanField(null=True)
	question_13_s3 = models.BooleanField(null=True)
	question_13_s4 = models.BooleanField(null=True)
	question_13_s5 = models.BooleanField(null=True)
	question_13_s6 = models.BooleanField(null=True)
	
	question_14 = models.IntegerField(null=True)
	question_15 = models.IntegerField(null=True)
	question_15_extra = models.TextField(blank=True, max_length=5000, null=True)
	

	def __str__(self):
		return f"Exam Result for {self.user.username}"





class ActividadEvaluativa(models.Model):
	name = models.CharField(max_length=60, null=True)
	descripcion = models.CharField(max_length=5000, null=True)
	alumno = models.ForeignKey("Alumno", on_delete=models.SET_NULL, null=True)
	curso = models.ForeignKey("Curso", on_delete=models.SET_NULL, null=True)
		
	def __str__(self):
		return f"{self.name}"


class Curso(models.Model):
	#pènsamiento o habilidades
	name = models.CharField(max_length=60, null=True)
	desc_short = models.CharField(max_length=5000, null=True)
	desc_detailed = models.CharField(max_length=5000, null=True)
	horarios = models.CharField(max_length=350, null=True)
	inicio = models.DateTimeField(null=True)
	cierre = models.DateTimeField(null=True)
	escuela = models.ForeignKey("Escuela", on_delete=models.SET_NULL, null=True)

	@property
	def alumnos(self):
		return Alumno.objects.filter(curso=self)
		
	def __str__(self):
		return self.name

class Escuela(models.Model):
	#e36 o e2
	name = models.CharField(max_length=60, null=True)
	localidad = models.CharField(max_length=255, null=True)
	@property
	def alumnos(self):
		return Alumno.objects.filter(escuela=self)
		
	def __str__(self):
		return f"{self.name}"


class Alumno(models.Model):
	#datos personales
	name = models.CharField(max_length=255, null=True)
	lastname = models.CharField(max_length=255, null=True)
	dni = models.PositiveIntegerField(null=True)
	localidad = models.CharField(max_length=255, null=True)
	nacimiento = models.DateField(null=True)
	email = models.EmailField(null=True)
	escuela = models.ForeignKey("Escuela", on_delete=models.SET_NULL, null=True)
	curso = models.ForeignKey("Curso", on_delete=models.SET_NULL, null=True)
	
	@property
	def edad(self):
		return date.today().year - self.nacimiento.year
		
	def __str__(self):
		return f"{self.name} {self.lastname}"
