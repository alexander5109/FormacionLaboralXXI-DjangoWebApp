from django.urls import path
from django.http import HttpResponse
from clan.views import *

app_name = "clan"

urlpatterns = [
	#ClanViews
	path('datos/',		Datos.as_view(), 			name='datos'),
	path('examen/',		Examen.as_view(), 			name='examen'),
	path('info/',		Info.as_view(), 			name='info'),
	path('home/',		Home.as_view(), 			name='home'),
	path('',			Home.as_view(),							),
]