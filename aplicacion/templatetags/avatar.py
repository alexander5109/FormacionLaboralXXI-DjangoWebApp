from django import template
from aplicacion import models

register = template.Library()

@register.filter(name="avatar")
def avatar(request):
	avatar_url = None
	try:
		avatar_url = models.AvatarPDF.objects.get(usuario = request.user.id).imagen.url
	except (Exception):
		try:
			avatar_url = models.Usuario.objects.get(id=request.user.id).avatar.url
		except (Exception):
			pass
	return avatar_url




	# return models.AvatarPDF.objects.get(usuario = request.user.id).imagen.url
	# if request.user.is_authenticated:
		# print("is_authenticated")
		# try:
			# print("trying")
			# instance = models.Usuario.objects.get(id=request.user.id)
			# try:
				# print("trying 2")
				# return instance.avatar.url
			# except (AttributeError, ValueError) :
				# pass
		# except (Exception): #models.Usuario.DoesNotExist:
			# try:
				# print(models.AvatarPDF.objects.get(usuario = request.user.id).imagen.url)
				# return models.AvatarPDF.objects.get(usuario = request.user.id).imagen.url
			# except (Exception):
				# return None

	# avatar_instance = models.AvatarPDF.objects.get(usuario = request.user.id).imagen.url
