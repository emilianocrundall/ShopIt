from django.urls import path
from shop import views
from .views import index, cat_obj, item_detalles, guardar_item, add_to_cart, ver_carrito, ver_favoritos, quitar_del_carrito, buscador, buscador_ajax, comentarios, categorias, vaciar_carro
from django.contrib.auth.decorators import login_required
app_name = 'shop'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:id>/items/', views.cat_obj, name='cat_obj'),
    path('categorias/', views.categorias, name='categorias'),
    path('<int:id>/items/detalles/', views.item_detalles, name='item_detalles'),
    path('<int:id>/guardar/', views.guardar_item, name='guardar'),
    path('<int:id>/agregar/', views.add_to_cart, name='add'),
    path('carrito/', login_required(views.ver_carrito), name='carrito'),
    path('favoritos/', login_required(views.ver_favoritos), name='favs'),
    path('<int:id>/quitar/', login_required(views.quitar_del_carrito), name='quitar'),
    path('buscar/', views.buscador, name='buscar'),
    path('resultadosajax/', views.buscador_ajax, name='buscar_ajax'),
    path('<int:id>/comentar/', login_required(views.comentarios), name='comentarios'),
    path('vaciar/', views.vaciar_carro, name='vaciar'),
]