from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from django.http import Http404, JsonResponse, HttpResponse
from django.contrib.auth.models import User
from .models import Item, OrderItem, Order, Review, Categoria
from django.db.models import Q
from django.db.models import Avg
import math
from django.views.decorators.csrf import csrf_protect

def index(request):
    cat = Categoria.objects.all()[:5]
    nuevos_ingresos = Item.objects.order_by("-id")[:4]
    return render(request, 'shop/index.html', {'cat': cat, 'nuevos': nuevos_ingresos})

def cat_obj(request, id):
    try:
        catobj = Categoria.objects.get(pk=id)
    except Categoria.DoesNotExist():
        raise Http404("La categoria no existe")
    return render(request, 'shop/cat_obj.html', {'catobj':catobj})

def categorias(request):
    try:
        cat = Categoria.objects.all()
    except Categoria.DoesNotExist():
        raise Http404("La categoria no existe")
    return render(request, 'shop/cats.html', {'cat':cat})

def item_detalles(request, id):
    is_favourite = False
    is_in_cart = False
    try:
        get_item = Item.objects.get(pk=id)
        get_comentarios = Review.objects.filter(item=get_item)
        avg_cal = get_comentarios.aggregate(average_rating=(Avg('calificacion')))
        if get_item.añadir_a_favs.filter(id=request.user.id).exists():
            is_favourite = True
        if OrderItem.objects.filter(user=request.user.id, item=get_item).exists():
            is_in_cart = True
    except Item.DoesNotExist:
        raise Http404('el item no existe')
    context = {
        'get_item':get_item,
        'is_favourite': is_favourite,
        'is_in_cart': is_in_cart,
        'comentarios': get_comentarios,
        'avg_cal': avg_cal
    }
    return render(request, 'shop/item.html', context)

def guardar_item(request, id):
    salida = {}
    item = get_object_or_404(Item, id=id)
    if item.añadir_a_favs.filter(id=request.user.id).exists():
        salida = {'quitar': True, 'msj': 'quitado'}
        item.añadir_a_favs.remove(request.user)
    else:
        item.añadir_a_favs.add(request.user)
        salida = {'agregar': True, 'msj': 'agregado'}
    return HttpResponse(JsonResponse(salida))

def ver_favoritos(request):
    favs = Item.objects.filter(añadir_a_favs=request.user.id)
    context = {'favs': favs}
    return render(request, 'shop/favoritos.html', context)

@csrf_protect
def add_to_cart(request,id):
    salida = {}
    if request.method == 'POST' and request.is_ajax():
        cantidad_ = request.POST.get('cantidad')
        try:
            item = get_object_or_404(Item, id=id)
            order_item = OrderItem.objects.create(item=item, user=request.user, cantidad=cantidad_)
            full_order = Order.objects.filter(user=request.user)
            if full_order.exists():
                order_qs = full_order[0]
                order_qs.items_ordered.add(order_item)
                salida = {'success': True, 'msj': 'Añadido al carrito'}
            else:
                ordered_date = timezone.now()
                order = Order.objects.create(user=request.user, fecha=ordered_date)
                order_item.save()
                order.items_ordered.add(order_item)
                salida = {'success': True, 'msj': 'Añadido al carrito'}
        except Item.DoesNotExist:
            salida = {'error': True, 'msj': 'El item no es recibido correctamente'}
    return HttpResponse(JsonResponse(salida))

@csrf_protect
def quitar_del_carrito(request, id):
    exit_ = {}
    try:
        item = get_object_or_404(Item, id=id)
        order = Order.objects.filter(user=request.user)
        if order.exists():
            order_qs = order[0]
            order_item = OrderItem.objects.filter(user=request.user.id, item=item)[0]
            order_qs.items_ordered.remove(order_item)
            order_item.delete()
            exit_ = {'exito': True, 'msj': 'Item quitado'}
        else:
            exit_ = {'error': True, 'msj': 'La orden no existe'}
    except Item.DoesNotExist:
        exit_ = {'error': True, 'msj': 'El item no es recibido correctamente'}
    return HttpResponse(JsonResponse(exit_))

@csrf_protect
def vaciar_carro(request):
    exit_ = {}
    try:
        order = Order.objects.filter(user=request.user)
        items_in_cart = OrderItem.objects.filter(user=request.user.id)
        items_in_cart.delete()
        order.delete()
        exit_ = {'success': True, 'msj': 'Carro Vacio'}
    except Order.DoesNotExist:
        exit_ = {'error': True, 'msj': 'La orden no es recibida correctamente'}
    return HttpResponse(JsonResponse(exit_))

def ver_carrito(request):
    carrito = Order.objects.filter(user=request.user)
    context = {'carrito': carrito}
    return render(request, 'shop/carrito.html', context)

def buscador(request):
    try:
        nombre_ = request.GET.get('q')
        obj = Item.objects.filter(nombre__icontains=nombre_)
    except Item.DoesNotExist:
        raise Http404('objetos no encontrados')
    return render(request, 'shop/resultados.html', {'objetos': obj})


def buscador_ajax(request):
    salida = {}
    item = request.GET.get('q')
    if request.is_ajax():
        objeto = Item.objects.filter(Q(nombre__icontains=item))
        resultados = []
        for obj in objeto:
            basic = {}
            basic['id'] = obj.id
            basic['nombre'] = obj.nombre
            resultados.append(basic)
        salida = {'exito': True, 'objetos': resultados}
    else:
        objeto = []
        salida = {'vacio': True, 'objetos': objeto}
    return HttpResponse(JsonResponse(salida))

@csrf_protect
def comentarios(request, id):
    salida = {}
    if request.method == 'POST' and request.is_ajax():
        texto_ = request.POST.get('texto')
        calificacion_ = request.POST.get('rating_value')
        try:
            item = get_object_or_404(Item, id=id)
            date = timezone.now()
            if texto_ and calificacion_:
                comentario = Review.objects.create(item=item, user=request.user, texto=texto_, fecha=date, calificacion=calificacion_)
                comentario.save()
                resultados = []
                basic = {}
                name_ = request.user.username
                basic['comentario'] = comentario.texto
                basic['user'] = name_
                basic['fecha'] = comentario.fecha
                basic['calificacion'] = comentario.calificacion
                resultados.append(basic)
                salida = {'exito': True, 'objetos': resultados}
            else:
                salida = {'error': True, 'msj': 'ups, parace que te has olvidado de dejar una calificacion'}
        except Item.DoesNotExist:
            salida = {'error': True, 'msj': 'El item no es recibido correctamente'}
    return HttpResponse(JsonResponse(salida))