from django.urls import path
from django.http import HttpResponse
from aplicacion.views import * # CursoCreateView
from django.conf import settings
from django.conf.urls.static import static

app_name = "aplicacion"

urlpatterns = [
	#login
	path('account/sign_up/',					Usuario_SignUp.as_view(),	name='user-sign_up'),
	path('account/log_in/',						Usuario_LogIn.as_view(),	name='user-log_in'),
	path('account/log_out/',					Usuario_LogOut.as_view(),	name='user-log_out'),
	path('account/cambiar_contraseña/',			Usuario_CambiarContraseña.as_view(),	name='user-cambiarcontraseña'),
	path('account/cambiar_avatar/',				Usuario_CambiarAvatar.as_view(),	name='user-cambiaravatar'),
	
	
	# CRUD experimento Many to many relationship.
	# path('cursos/<slug:slug>/sumar_alumno', 	CursoSumaAlumno.as_view(_tables="cursos"),	name='cursos-sumar_alumno'),
	
	
	
	
	# CRUD usando generic view classes.
	path('centros_de_formacion/list/',			Centros_List.as_view(),		name='centros-list'),
	path('centros_de_formacion/detail/<pk>',	Centros_Detail.as_view(),	name='centros-detail'),
	path('centros_de_formacion/delete/<pk>',	Centros_Delete.as_view(),	name='centros-delete'),
	path('centros_de_formacion/update/<pk>',	Centros_Update.as_view(),	name='centros-update'),
	path('centros_de_formacion/create/',		Centros_Create.as_view(),	name='centros-create'),
	
	
	# CRUD usando mis propias funciones que funcionan para Curso y Estudiante.
	path('<str:tables>/buscador/buscar', 		Tables_Buscar.as_view(),	name='tables-buscar'),
	path('<str:tables>/buscador/', 				Tables_Buscador.as_view(), 	name='tables-buscador'),
	path('<str:tables>/create/',				Tables_Agregar.as_view(),	name='tables-create'),
	path('<str:tables>/<slug:slug>/read', 		Tables_Detalle.as_view(),	name='tables-read'),
	path('<str:tables>/<slug:slug>/edit', 		Tables_Editar.as_view(), 	name='tables-update'),
	path('<str:tables>/<slug:slug>/delete', 	Tables_Eliminar.as_view(), 	name='tables-delete'),
	path('<str:tables>/listado/', 				Tables_Listado.as_view(), 	name='tables-listado'),
	
	# Estos son los que menos prioridad tienen..
	path('<int:error_code>/', 					codigos_view, 				name='codigo'),
	path('quejas/', 							Quejas.as_view(), 			name='quejas'),
	path('about/', 								About.as_view(), 			name='about'),
	path('home/', 								Home.as_view(), 			name='home'),
	path('',				 					Home.as_view(),							),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)