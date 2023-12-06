from django.urls import path
from django.http import HttpResponse
from blog import views # CursoCreateView
from django.conf import settings
from django.conf.urls.static import static

app_name = "blog"

urlpatterns = [
	path('<slug:slug>/', views.post_detail, name='post_detail'),
    # path('<slug:slug>/',	views.PostDetail.as_view(), 	name='post_detail'),
	path('',				views.PostList.as_view(),					name="home"),
]
