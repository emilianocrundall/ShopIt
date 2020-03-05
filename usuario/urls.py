from django.urls import path
from usuario import views
from .views import usuario_nuevo, index, login
from django.contrib.auth.decorators import login_required

app_name = 'usuario'

urlpatterns = [
    path('index/', login_required(views.index), name='index'),
    path('registrar/', views.usuario_nuevo, name='nuevo'),
    path('login/', views.login_user, name='log'),
]