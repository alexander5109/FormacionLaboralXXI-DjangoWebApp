from django.contrib import admin
from django.db.models import Count
from . import models
# Register your models here.



@admin.register(models.Institucion)
class InstitucionAdmin(admin.ModelAdmin):
	list_display = ('name', 'partido', 'cuya_provincia', 'cuyos_cursos', 'id')
	def cuya_provincia(self, obj):
		return f"{obj.partido.provincia}"
	def cuyos_cursos(self, obj):
		yogurt = models.Curso.objects.filter(institucion=obj)
		return {curso.name for curso in yogurt}



@admin.register(models.Estudiante)
class EstudianteAdmin(admin.ModelAdmin):
	list_display = ('name', 'lastname', 'age', 'slug', 'id', 'updated', 'created')



@admin.register(models.Curso)
class CursoAdmin(admin.ModelAdmin):
	list_display = ('name', 'familia_profesional', "institucion", 'slug', 'id')
	# def estudiantes(self, obj):
		# return ", ".join([f"{count}: {student}" for count, student in enumerate(obj.alumnos, start=1)])
	# estudiantes.short_description = 'Alumnos'



@admin.register(models.Provincia)
class ProvinciaAdmin(admin.ModelAdmin):
	list_display = ('name', 'display_partidos', 'id')
	def display_partidos(self, obj):
		return ", ".join([partido.name for partido in obj.partidos])
	display_partidos.short_description = 'Partidos'



@admin.register(models.FamiliaProfesional)
class FamiliaProfesionalAdmin(admin.ModelAdmin):
	list_display = ('name', 'cuyos_cursos', 'id')
	def cuyos_cursos(self, obj):
		yogurt = models.Curso.objects.filter(familia_profesional=obj)
		return {curso.name for curso in yogurt}



@admin.register(models.Partido)
class PartidoAdmin(admin.ModelAdmin):
	# list_display = ('name', 'provincia', "total_de_cursos", "total_de_alumnos")
	list_display = ('name', 'provincia', 'id')
	
	## help here
	
	#yo quiero que me devuelva Todos las instancias de "Curso" cuyo "institucion" cuyo "partido" sea este
	
	
	
	 
# @admin.register(models.Avatar)
# class AvatarAdmin(admin.ModelAdmin):
	# pass
	 
@admin.register(models.Usuario)
class UsuarioAdmin(admin.ModelAdmin):
	pass	
	
@admin.register(models.AvatarPDF)
class AvatarAdmin(admin.ModelAdmin):
	pass
	
@admin.register(models.Queja)
class QuejaAdmin(admin.ModelAdmin):
	pass
	
	
	
	
	
	"""
	Curso.objects.filter(Curso.institucion.partido = obj)
	
	def total_de_cursos(self, obj):
		# return Curso.objects.all().count()
		return Curso.objects.get(institucion)
	def total_de_alumnos(self, obj):
		return "Banana?"
		# return Estudiante.objects.all().count()
		# return Estudiante.objects.all().filter(partido=obj)
	"""
