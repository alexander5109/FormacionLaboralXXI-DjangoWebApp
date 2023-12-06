from django import forms
from django.contrib import auth
from . import models
# from django.core.validators import EmailValidator

#Obsolete now
"""
class EstudianteFormulario(forms.Form):
	name = forms.CharField(label='Nombre', max_length=255)
	lastname = forms.CharField(label='Apellido', max_length=255)
	nacimiento = forms.DateField(label='Fecha de Nacimiento', widget=forms.DateInput(attrs={'type': 'date'}))
	email = forms.EmailField(label='Email', validators=[EmailValidator(message='Correo invalido')])
	phone = forms.CharField(label='Telefono', required=False, max_length=20)
	curso = forms.ChoiceField(
		label='Curso', 
		choices=[(campo.id, campo.name) for campo in models.Curso.objects.all()]
		)
	
class CursoFormulario(forms.Form):
	name = forms.CharField(label='Nombre', max_length=255)
	descripcion = forms.CharField(label='Descripción', max_length=5000, widget=forms.Textarea(attrs={'rows': 4, 'cols': 40}))
	familia_profesional = forms.ChoiceField(
		label='Familia Profesional', 
		choices=[(campo.id, campo.name) for campo in models.FamiliaProfesional.objects.all()]
		)
	institucion = forms.ChoiceField(
		label = 'Institución en que se dicta', 
		choices = [(campo.id, campo.name) for campo in models.Institucion.objects.all()]
		)
"""
	
	

class NewEstudianteModelForm(forms.ModelForm):
	class Meta:
		model = models.Estudiante
		# fields = ['name', 'lastname', 'nacimiento', 'email', 'phone', 'cursos'] #todos
		exclude = ["slug"]
		widgets = {
					'nacimiento': forms.DateInput(attrs={'type': 'date'})
					}
		labels = {	
					"name": "Nombre",
					"lastname": "Apellido",
					"nacimiento": "Fecha de Nacimiento",
					"email": "Email",
					"phone": "Teléfono",
					"cursos": "Cursos",
		}

class NewCursoModelForm(forms.ModelForm):
	class Meta:
		model = models.Curso
		exclude = ["slug"]
		labels = {	
					"name": "Nombre",
					"descripcion": "Descripción",
					"familia_profesional": "Familia Profesional",
					"institucion": "Instituto que lo dicta",
					"estudiantes": "Estudiantes",
		}



class InstitucionForm(forms.ModelForm):
	class Meta:
		model = models.Institucion
		fields = ["name", "partido", "cue"]
		labels = {
					"name": "Nombre",
					"partido": "Partido",
					"cue": "Codigo Unico de Escuela",
			}
			
# class RegistroDeUsuarioForm(forms.ModelForm):

	# class Meta:
		# model = models.Usuario
		# fields = [
			# 'title',
			# 'artist',
			# 'release_date',
			# 'logo'
		# ]
			
class RegistroDeUsuarioForm(auth.forms.UserCreationForm):
	# pass
	error_messages = {
		"password_mismatch": "Las contraseñas no coinciden.",
		"unique": "Ya existe alguien con ese nombre de usuario.",	##no funa este. el de las pass si.
	}
	
	email = forms.EmailField()
	username = forms.CharField(min_length=5, max_length=18, strip=True, label="Usuario")
	first_name = forms.CharField(min_length=1, max_length=155, label="Nombre")
	last_name = forms.CharField(min_length=1, max_length=155, label="Apellido")
	password1 = forms.CharField(label="Contraseña", widget=forms.PasswordInput)
	password2 = forms.CharField(label="Repetir contraseña", widget=forms.PasswordInput)
	# avatar = forms.ImageField()
	
	class Meta:
		model = models.Usuario # auth.models.User #;;:;; not noww ;;; models.Usuario
		fields = [
			"username",
			"first_name",
			"last_name",
			"email",
			"password1",
			"password2",
			"avatar",	#que lo lea desde el model
			]
		# help_texts = {a: "" for a in fields}
		
class CambiarAvatarForm(forms.ModelForm):
	# pass
	error_messages = {
		"password_mismatch": "Las contraseñas no coinciden.",
		# "unique": "Ya existe alguien con ese nombre de usuario.",	##no funa este. el de las pass si.
	}
	
	# email = forms.EmailField()
	# username = forms.CharField(min_length=5, max_length=18, strip=True, label="Usuario")
	# first_name = forms.CharField(min_length=1, max_length=155, label="Nombre")
	# last_name = forms.CharField(min_length=1, max_length=155, label="Apellido")
	# password1 = forms.CharField(label="Contraseña", widget=forms.PasswordInput)
	# password2 = forms.CharField(label="Repetir contraseña", widget=forms.PasswordInput)
	# avatar = forms.ImageField()
	
	class Meta:
		model = models.Usuario # auth.models.User #;;:;; not noww ;;; models.Usuario
		# exclude = ["id"]
		fields = [
			# "username",
			# "first_name",
			# "last_name",
			# "email",
			# "password1",
			# "password2",
			"avatar",	#que lo lea desde el model
			]
	# fields += ["avatar"]

class UserSettingsForm(auth.forms.PasswordChangeForm):
	# class Meta:
		# model = models.Usuario # auth.models.User #;;:;; not noww ;;; models.Usuario
		# fields = [
			# "password1",
			# "password2",
			# "avatar",	#que lo lea desde el model
			# ]
	pass
	# fields += ["avatar"]



class AutentificacionForm(auth.forms.AuthenticationForm):
	error_messages = {
        'invalid_login': 'El usuario no existe o la contraseña es incorrecta.',
    }
	
	
# class CursoSumaEstudianteForm(forms.Form):
	# pass
	# slug = 
 

class NewQuejaForm(forms.ModelForm):
	class Meta:
		model = models.Queja
		exclude = ["id", "atendido"]
		labels = {	
					"nombre": "Nombre y apellido",
					"dni": "DNI",
					"email": "Correo electronico",
					"mensaje": "Retroalimentación",
		}