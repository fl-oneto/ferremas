from django.shortcuts import render
from django.http import HttpResponse
from .models import Categoria, Producto, Rol, Usuario, Region, Comuna, Direccion, Telefono, UnidadMedida, Carrito, ItemCarrito, Pedido, DetallePedido, MetodoPago, Pago

def home(request):
    categorias = Categoria.objects.all()
    return render(request, 'home.html', {'categorias': categorias})


