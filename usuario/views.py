from django.shortcuts import render
from django.contrib.auth.models import User
import re
from django.http import HttpResponse, JsonResponse
from .forms import UsuarioForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import check_password

def index(request):
    return render(request, 'usuario/index.html')

def usuario_nuevo(request):
    salida = {}
    if request.method == 'POST' and request.is_ajax():
        form = UsuarioForm(request.POST)
        username_ = request.POST.get('username')
        first_name_ = request.POST.get('first_name')
        last_name_ = request.POST.get('last_name')
        password_ = request.POST.get('password')
        password2 = request.POST.get('password2')
        email_ = request.POST.get('email')

        if not password_ and not email_ and not first_name_ and not last_name_ and not username_:
            salida = {'error': True, 'msj': 'por favor completa los campos'}
        if password_ and email_ and first_name_ and last_name_ and username_:
            ex_regular = r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$"
            if re.match(ex_regular, email_):
                if len(password_) > 6:
                    if password_ == password2:
                        if not(User.objects.filter(username=username_).exists() or User.objects.filter(email=email_).exists()):
                            new_user = User.objects.create(username=username_, first_name=first_name_, last_name=last_name_, email=email_, password=password_)
                            new_user.set_password(request.POST.get('password'))
                            new_user.save()
                            new_user = authenticate(username=username_, password=password_)
                            login(request, new_user)
                            salida = {'exito': True, 'msj': 'success'}
                        else:
                            salida = {'error': True, 'msj': 'Ese nombre de usuario y/o email ya estan registrados'}
                    else:
                        salida = {'error': True, 'msj': 'Las contraseñas no coinciden'}
                else:
                    salida = {'error': True, 'msj': 'La contraseña es muy corta, intenta con otra'}
            else:
                salida = {'error': True, 'msj': 'Ingrese un email valido'}
        else:
            salida = {'error': True, 'msj': 'por favor completa los campos'}
    else:
        form = UsuarioForm()
    return HttpResponse(JsonResponse(salida))

def login_user(request):
    salida = {}
    if request.method == 'POST' and request.is_ajax():
        username_ = request.POST.get('username')
        password_ = request.POST.get('password')
        if not username_ and not password_:
            salida = {'error': True, 'msj': 'Por favor llena los campos correctamente'}
        if username_ and password_:
            try:
                get_usuario = User.objects.get(username=username_)
                get_password = get_usuario.password
                if check_password(password_, get_password):
                    user = authenticate(username=username_, password=password_)
                    if user is not None:
                        login(request, user)
                        salida = {'success': True, 'msj': 'exito'}
                else:
                    salida = {'error': True, 'msj': 'Contraseña incorrecta'}
            except User.DoesNotExist:
                salida = {'error': True, 'msj': 'El usuario con el que quieres ingresar no esta registrado'}
        else:
            salida = {'error': True, 'msj': 'Por favor llena los campos correctamente'}
    return HttpResponse(JsonResponse(salida))


