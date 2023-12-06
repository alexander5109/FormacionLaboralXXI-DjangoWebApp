from . import models
from django import forms



class CommentForm(forms.ModelForm):
	class Meta:
		model = models.Comment
		fields = ('name', 'email', 'body')
		labels = {	
					"name": "Nombre",
					"body": "Comentario",
					"email": "Correo electronico",
		}