from django.shortcuts import render, redirect, get_object_or_404
from django.template import TemplateDoesNotExist
from django.urls import reverse
from django.db.models import Q
from django.views import View, generic
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.utils.html import escape
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from . import models, forms
from functools import wraps
import random
from django.shortcuts import resolve_url
# Create your views here.
from django.utils.safestring import mark_safe


# //--------------------------------------------------------------------//
# ;;--------------------------decoradores---------------------------;;
# //--------------------------------------------------------------------//


def return_404_if_no_template(func):
	@wraps(func)
	def wrapper(self, request, *args, **kwargs):
		try:
			return func(self, request, *args, **kwargs)
		except TemplateDoesNotExist:
			return redirect(reverse('aplicacion:codigo', args=['404']))
	return wrapper


# //--------------------------------------------------------------------//
# ;;--------------------------Funciones Views---------------------------;;
# //--------------------------------------------------------------------//

def codigos_view(request, error_code):
	#no me anduvo el decorator para este.
	template = f"aplicacion/{error_code}.html"
	try:
		return render(request, template)
	except TemplateDoesNotExist:
		template = f"aplicacion/404.html"
		return render(request, template)
	
	

# //--------------------------------------------------------------------//
# ;;------------------------Generic Template View-----------------------;;
# //--------------------------------------------------------------------//
	
	
class Home(generic.TemplateView):
	template_name="aplicacion/t2_home.html"
		
class About(generic.TemplateView):
	template_name="aplicacion/t2_about.html"
		
		

# //--------------------------------------------------------------------//
# ;;--------------------------My Main View-------------------------;;
# //--------------------------------------------------------------------//
class MyLoginRequiredMixin(LoginRequiredMixin):
	login_url = 'aplicacion:user-log_in'
	signup_url = 'aplicacion:user-sign_up'
	home_url = 'aplicacion:home'


class MyViewMaster(View):
	success_template = "aplicacion/201.html"
	failure_template = "aplicacion/400.html"
	login_url = 'aplicacion:user-log_in'
	signup_url = 'aplicacion:user-sign_up'
	home_url = 'aplicacion:home'
	_form = None
	_user_pk = None
	_instance = None
	_model = None
	_item_buscado = None
	
	@property
	def item_buscado(self):
		if self._item_buscado is None:
			self._item_buscado = escape(self.request.GET.get('search'))
		return self._item_buscado
	@property
	def form(self):
		if self._form is None:
			# request_post = self.request.POST or None
			# self._form = self.form_model(request_post) if request_post else self.form_model()
			self._form = self.form_model(self.request.POST, self.request.FILES, instance=self.instance)
		return self._form
	@property
	def user_pk(self):
		if self._user_pk is None:
			self._user_pk = self.request.user.pk
		return self._user_pk
	@property
	def instance(self):
		if self._instance is None:
			self._instance = self.model.objects.get(pk=self.user_pk)
		return self._instance
		
	@property
	def slug(self):
		return self.kwargs.get("slug")
	@property
	def previous_url(self):
		return self.request.META.get('HTTP_REFERER')
	@property
	def next_url(self):
		return self.request.GET.get('next')
								
						
# //--------------------------------------------------------------------//		

class MyTablesViewMaster(MyViewMaster):
	_tables = None
	_instance = None
	_form = None
	@property
	def tables(self):
		if self._tables is None:
			self._tables = self.kwargs.get("tables")
		return self._tables
	@property
	def table(self):
		return "curso" if self.tables == "cursos" else "estudiante" if self.tables == "estudiantes" else None
	@property
	def model(self):
		return models.Curso if self.tables == "cursos" else models.Estudiante if self.tables == "estudiantes" else None
	@property
	def form_model(self):
		return forms.NewCursoModelForm if self.tables == "cursos" else forms.NewEstudianteModelForm if self.tables == "estudiantes" else None
	@property
	def instance(self):
		if self._instance is None:
			if self.slug and self.model:
				self._instance = self.model.objects.get(slug=self.slug)
		return self._instance
	@property
	def form(self):
		if self._form is None:
			if self.instance and self.request:
				self._form = self.form_model(self.request.POST or None, instance=self.instance)
			elif self.request:
				self._form =  self.form_model(self.request.POST or None)
			elif self.instance:
				self._form =  self.form_model(instance=self.instance)
			else:
				self._form =  self.form_model()
		return self._form
	def buscar_item(self):
		if self.model == models.Estudiante:
			return self.model.objects.filter(	
								Q(name__iexact=self.item_buscado) | 
								Q(name__icontains=self.item_buscado) | 
								Q(lastname__iexact=self.item_buscado) | 
								Q(lastname__icontains=self.item_buscado)
								)
		elif self.model == models.Curso:
			return self.model.objects.filter(	
								Q(name__icontains=self.item_buscado) | 
								Q(familia_profesional__name__icontains=self.item_buscado)
								#interesante: para hacer una query sobre el campo "nombre" de la foreing key vinculada, se le vuelve a escribir __name para acceder a los campos del objeto." Seria algo como "curso.familia_profesional.name contains item_buscado"
								)


# //--------------------------------------------------------------------//

	
class Quejas(MyViewMaster, generic.TemplateView):
	template_name="aplicacion/t2_quejas.html"
	model = models.Queja
	form_model = forms.NewQuejaForm
	_form = None
	@property
	def form(self):
		if self._form:
			return self._form
		request_post = self.request.POST or None
		self._form =  self.form_model(request_post) if request_post else self.form_model()
		return self._form
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['form'] = self.form
		return context
	
	def post(self, request):
		#if post, we instance it filled.
		if self.form.is_valid():
			self.form.save()			##guardar para generar id.
			# instance.save_new_slug()	##ya No hace falta. Puse que se aplique sobre el save() original. ##generar slug en base a id. necesaria para links personalizados
			mensaje = self.form.cleaned_data.get("mensaje")
			usuario = self.form.cleaned_data.get("nombre")
			contexto = {
						'success_header_1': f"Querid@ {usuario}...",
						'success_header_2': f"Tu queja fue enviada",
						'success_message': f'El mensaje "{mensaje[:20]}[...]" ha sido correctamente recibido en nuestra base de datos... Anda a saber cuando te respondemos.',
						'button_msg': f"Volver a la Home",
						'button_url': reverse(self.home_url),
			}
			return render(request, self.success_template, contexto)
		else:
			#si hubo un error, te devuelvo la misma pagina como si fuera get. pero con los datos que se llegaron a cargar para que sean corregidos.
			print(self.form)
			contexto = {"form": self.form}
			return render(request, self.template_name, contexto)
		
		

# //--------------------------------------------------------------------//
		
		
class Tables_Buscar(MyTablesViewMaster):
	@return_404_if_no_template
	def get(self, request, tables):
		template = f"aplicacion/t2_{tables}_buscador.html"
		contexto = {
					"item_buscado": self.item_buscado, 
					"results": self.buscar_item(), 
					}
		return render(request, template, contexto)


# //--------------------------------------------------------------------//

class Tables_Agregar(MyLoginRequiredMixin, MyTablesViewMaster):
	@return_404_if_no_template
	# @method_decorator(login_required(login_url='aplicacion:user-log_in'))
	def get(self, request, tables):
		template = f"aplicacion/t2_{tables}_add.html"
		contexto = {"form": self.form}
		return render(request, template, contexto)

	def post(self, request, tables):
		#if post, we instance it filled.
		if self.form.is_valid():
			self.form.save()			##guardar para generar id.
			# instance.save_new_slug()	##ya No hace falta. Puse que se aplique sobre el save() original. ##generar slug en base a id. necesaria para links personalizados
			contexto = {
						'success_header_1': f"Instancia agregada exitosamente.",
						'success_header_2': f"{self.form.instance.name} fue agregada",
						'success_message': f"<strong> {self.form.instance} </strong> fue correctamente agregado a la base de datos de este sitio",
						'button_msg': f"Volver al listado de {self.tables.capitalize()}",
						'button_url': reverse('aplicacion:tables-listado', args=[tables]),
			}
			return render(request, self.success_template, contexto)
		else:
			#si hubo un error, te devuelvo la misma pagina como si fuera get. pero con los datos que se llegaron a cargar para que sean corregidos.
			template = f"aplicacion/t2_{tables}_add.html"
			contexto = {"form": self.form}
			return render(request, template, contexto)


# //--------------------------------------------------------------------//
class Tables_Editar(MyLoginRequiredMixin, MyTablesViewMaster):
	@return_404_if_no_template
	# @method_decorator(login_required(login_url='aplicacion:user-log_in'))
	def get(self, request, tables, slug):
		#create a form with new data, OVER the instance with the slug. If get, we instance it empty, if post, we instance it filled.
		template = f"aplicacion/t2_{tables}_edit.html"
		contexto = {
					"form": self.form,
					"instance": self.instance
					}
		return render(request, template, contexto)

	def post(self, request, tables, slug):
		if self.form.is_valid():
			self.form.save()			##el form llama a su instancia de modelo y guarda los cambios.
			contexto = {
						'success_header_1': f"Datos modificados exitosamente.",
						'success_header_2': f"{self.form.instance.name} fue modificado",
						'success_message': f"<strong> {self.form.instance} </strong> fue correctamente modificado en la base de datos de este sitio",
						'button_msg': f"Volver a detalles de {self.instance.name} ",
						'button_url': reverse('aplicacion:tables-read', args=[tables, self.instance.slug]),
			}
			return render(request, self.success_template, contexto)
		else:
			#si hubo un error, te devuelvo la misma pagina como si fuera get. pero con los datos que se llegaron a cargar para que sean corregidos.
			template = f"aplicacion/t2_{tables}_edit.html"
			contexto = {
						"form": self.form,
						"instance": self.instance
						}
			return render(request, template, contexto)


# //--------------------------------------------------------------------//

class Tables_Detalle(MyTablesViewMaster):
	@return_404_if_no_template
	def get(self, request, tables, slug):
		contexto = {
					self.table: self.instance
					}
		template = f"aplicacion/t2_{tables}_details.html"
		return render(request, template, contexto)
		
		

# //--------------------------------------------------------------------//

class Tables_Eliminar(MyLoginRequiredMixin, MyTablesViewMaster):
	@return_404_if_no_template
	# @method_decorator(login_required(login_url='aplicacion:user-log_in'))
	def get(self, request, tables, slug):
		template = f"aplicacion/t2_{tables}_details.html"
		contexto = {
					self.table: self.instance,
					"confirm_deletion": True,
					}
		return render(request, template, contexto)
			
	def post(self, request, tables, slug):
		#la success template viene de MyTablesViewMaster.. 
		self.instance.delete()			##delete from the db.sqlite3 file
		contexto = {
					'success_message': f"<strong> {self.instance} </strong> fue eliminado en la base de datos de este sitio",
					'button_msg': f"Volver al listado de {self.tables.capitalize()} ",
					'button_url': reverse('aplicacion:tables-listado', args=[tables]),
		}
		return render(request, self.success_template, contexto)


# //--------------------------------------------------------------------//

class Tables_Listado(MyTablesViewMaster):
	@return_404_if_no_template
	def get(self, request, tables):
		template = f"aplicacion/t2_{tables}_listado.html"
		contexto = {}
		if self.model:
			#estas dos opciones son si los quiero shufflear o ordenar por nombre.
			#ordneadollaros# data = data.objects.all().order_by('name')
			#randomizarlos# random.shuffle(list(data))
			contexto = {self.tables: self.model.objects.all()}
		return render(request, template, contexto)


# //--------------------------------------------------------------------//
class Tables_Buscador(MyTablesViewMaster):
	@return_404_if_no_template
	def get(self, request, tables):
		template = f"aplicacion/t2_{tables}_buscador.html"
		contexto = {}
		return render(request, template, contexto)
		
		
		
		
		
		
		
		
		
		
		



	


# //--------------------------------------------------------------------//
# ;;--------------------------Generic Views-------------------------;;
# //--------------------------------------------------------------------//

#01
# //---------------------//
class Centros_List(generic.ListView):
	model = models.Institucion
	# queryset = models.Institucion.objects.all()
	# context_object_name  = "instituciones"	//el prefijo es "institucion_list"

#02
# //---------------------//
class Centros_Create(MyLoginRequiredMixin, generic.CreateView):
	model = models.Institucion
	form_class = forms.InstitucionForm
	template_name = "aplicacion/institucion_create.html"
	# success_url = "/institucion_list"
	# fields = ["name", "partido", "cue"]
	# queryset = models.Institucion.objects.all()
	
	def form_valid(self, form):
		self.object = form.save()
		return redirect(reverse('aplicacion:codigo', args=["201"]))
		
	# def get_context_data(self, **kwargs):
		# contexto = super().get_context_data(**kwargs)
		# return contexto

		
#03
# //---------------------//
class Centros_Detail(generic.DetailView):
	model = models.Institucion
	
#04
# //---------------------//
class Centros_Delete(MyLoginRequiredMixin, generic.DeleteView):
	model = models.Institucion
	# success_url = reverse('aplicacion:centros-list')

	def get_success_url(self):
		return reverse('aplicacion:codigo', args=["201"])

#05
# //---------------------//
class Centros_Update(MyLoginRequiredMixin, generic.UpdateView):
	model = models.Institucion
	# success_url = "/institucion_list"
	fields = ["name", "partido", "cue"]
	
	
	


# //--------------------------------------------------------------------//
# ;;--------------------------Logins-------------------------;;
# //--------------------------------------------------------------------//


class Usuario_SignUp(MyViewMaster):
	LOGIN_AFTER_SIGNUP = True
	template =  "aplicacion/t2_user_sign_up.html"
	success_template = "aplicacion/201.html"
	failure_template = "aplicacion/400.html"
	model = models.Usuario
	form = forms.RegistroDeUsuarioForm
	def post(self, request):
		self.form = self.form(request.POST, request.FILES)
		if self.form.is_valid():
			username = self.form.cleaned_data.get("username")
			self.form.save()
			if not self.LOGIN_AFTER_SIGNUP:
				contexto = {
							'success_header_1': f"Instancia agregada exitosamente.",
							'success_header_2': f"{username} fue agregado",
							'success_message': f"<strong> {username} </strong> fue correctamente agregado a la base de datos de este sitio. \n Ya puede iniciar sesión.",
							'button_msg': f"Iniciar sesión",
							'button_url': reverse(self.login_url),
				}
				return render(request, self.success_template, contexto)
			else:
				return redirect(self.login_url)
		else:
			#si hubo un error, te duelvo a la misma pagina como si fuera un get. pero te mando lo que se llegó a cargar del formulario para que el usuario lo corrija. Los errores son mostrados con colorcitos por la template.
			contexto = {"form": self.form}
			return render(request, self.template, contexto)
			
	def get(self, request):
		self.form = self.form()
		contexto = {"form": self.form}
		return render(request, self.template, contexto)


class Usuario_LogIn(auth.views.LoginView):
	template_name = "aplicacion/t2_user_log_in.html"
	authentication_form = forms.AutentificacionForm
	model = models.Usuario

	def get_success_url(self):
		#Si la pagina previa era login o signup, devolver a home. Sino volver a donde la url pedia con "?=next", lo cual lo recibe desde el link en la nav bar de 0000_master.html
		if next_url:= self.request.GET.get('next') in {reverse('aplicacion:user-log_in'), reverse('aplicacion:user-sign_up')}:
			return reverse('aplicacion:home')
		elif next_url:
			return next_url
		else:
			return reverse('aplicacion:home')
		
			
class Usuario_LogOut(auth.views.LogoutView, MyViewMaster):
	template_name =  "aplicacion/t2_user_log_out.html"
	def get(self, request):
		#Si se puede calcular la url previa, nos devuelve ahí. Sino, usamos devolvemos el metodo get() original de django auth.views.LogoutView
		auth.logout(request)
		if self.previous_url:
			return redirect(self.previous_url)
		else:
			return super().get(request)

		
		
		
		
		
	
	
# //--------------------------------------------------------------------//
"""
class CursoSumaAlumno(MyLoginRequiredMixin, MyViewMaster):
	def get(self, request, slug):
		template = f"aplicacion/WiP/t2_cursos_sumaralumno.html"
		contexto = {}
		self.model = models.Curso
		if self.model:
			contexto = {
						"instance": self.instance,
						"estudiantes": models.Estudiante.objects.exclude(),
						# "form": CursoSumaEstudianteForm(),
						} 
		return render(request, template, contexto)

	def post(self, request, slug):
		template = f"aplicacion/WiP/t2_cursos_sumaralumno.html"
		contexto = {}
		self.model = models.Curso
		if self.model:
			contexto = {
						"cursos": self.model.objects.all(),
						}
		return render(request, template, contexto)
"""



# //--------------------------------------------------------------------//
class Usuario_CambiarContraseña(MyLoginRequiredMixin, auth.views.PasswordChangeView, MyViewMaster):
	template_name = "aplicacion/t2_user_change_pw.html"
	form_class = forms.UserSettingsForm
	def get_success_url(self):
		return reverse('aplicacion:codigo', args=["201"])
	
	

# //--------------------------------------------------------------------//
class Usuario_CambiarAvatar(MyLoginRequiredMixin, MyViewMaster):
	template = "aplicacion/t2_user_change_avatar.html"
	model = models.Usuario
	form_model = forms.CambiarAvatarForm
	success_template = "aplicacion/201.html"
	home_url = 'aplicacion:home'
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['form'] = self.form
		return context
	
	def get(self, request):
		contexto = {
					"form": self.form_model(),
					} 
		return render(request, self.template, contexto)
	
	def post(self, request):
		if self.form.is_valid():
			self.form.save()
			contexto = {
						'success_header_1': f"Querid@ {request.user.username}...",
						'success_header_2': f"Tu avatar fue cambiado",
						'success_message': f'Saludos',
						'button_msg': f"Volver a la Home",
						'button_url': reverse(self.home_url),
			}
			return render(request, self.success_template, contexto)
		else:
			contexto = {"form": self.form}
			return render(request, self.template, contexto)
	
	

# //--------------------------------------------------------------------//