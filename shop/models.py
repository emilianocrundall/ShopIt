from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal
from django.db.models import F, Sum

Metodos = (
    ('td', 'Tarjeta de Debito'),
    ('ef', 'Efectivo'),
    ('tc', 'Tarjeta de Credito')
)
class Categoria(models.Model):
    nombre = models.CharField(max_length=200)

    def __str__(self):
        return(self.nombre)

class Item(models.Model):
    nombre = models.CharField(max_length=100)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    imagen = models.ImageField(blank=True, null=True, upload_to='covers/%Y/%m/%D/')
    precio = models.FloatField()
    descripcion = models.TextField()
    añadir_a_favs = models.ManyToManyField(User, related_name='fav_items', blank=True)

    def __str__(self):
        return self.nombre

class OrderItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    cantidad = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.cantidad} of {self.item.nombre}"

    def total_item(self):
        return self.cantidad * self.item.precio

class Direccion(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    provincia = models.CharField(max_length=100)
    localidad = models.CharField(max_length=100)
    codigo_postal = models.IntegerField()
    direccion = models.CharField(max_length=70)

class Order(models.Model):
    items_ordered = models.ManyToManyField(OrderItem)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    fecha = models.DateField(auto_now_add=True)
    direccion_envio = models.ForeignKey(Direccion, on_delete=models.CASCADE, null=True)

    def get_items(self):
        return(self.items_ordered.all())

    def get_total(self):
        total = 0
        for order_item in self.items_ordered.all():
            total += order_item.total_item()
        return total

class Review(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    texto = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha = models.DateField(auto_now_add=True)
    calificacion = models.IntegerField(default=1)

    def __str__(self):
        return self.texto