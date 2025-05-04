from django import forms
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Categoria, Producto, Region, Comuna, Direccion, Telefono, UnidadMedida, Carrito, ItemCarrito, Pedido, DetallePedido, MetodoPago, Pago
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm, EmailLoginForm
from django.contrib.auth.decorators import login_required

def login_view(request):
    if request.method == 'POST':
        form = EmailLoginForm(request.POST)
        if form.is_valid():
            login(request, form.user)
            return redirect('home')
    else:
        form = EmailLoginForm()
    return render(request, 'registro/login.html', {'form': form})


def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # inicia sesión después del registro
            return redirect('login')  # ajusta esta ruta según tu app
    else:
        form = CustomUserCreationForm()
    return render(request, 'registro/signup.html', {'form': form})


def home(request):
    categorias = Categoria.objects.all()
    productos = Producto.objects.all()

    context = {
        'categorias': categorias,
        'productos': productos,
     }
    return render(request, 'home.html', context)

@login_required
def myaccount(request):
    return render(request, 'myaccount.html')

def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Producto, pk=producto_id)
    cantidad = int(request.POST.get('cantidad', 1))

    if request.user.is_authenticated:
        # Carrito por usuario logueado
        carrito, creado = Carrito.objects.get_or_create(usuario=request.user)
    else:
        # Carrito por sesión
        if not request.session.session_key:
            request.session.create()
        session_key = request.session.session_key
        carrito, creado = Carrito.objects.get_or_create(session_key=session_key)

    item, creado = ItemCarrito.objects.get_or_create(carrito=carrito, producto=producto)

    if not creado:
        item.cantidad += cantidad
    else:
        item.cantidad = cantidad

    item.save()
    return redirect('ver_carrito')



def ver_carrito(request):
    lista_items = []
    items = []
    total = 0

    if request.user.is_authenticated:
        try:
            carrito = Carrito.objects.get(usuario=request.user)
        except Carrito.DoesNotExist:
            carrito = None
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        try:
            carrito = Carrito.objects.get(session_key=session_key)
        except Carrito.DoesNotExist:
            carrito = None

    if carrito:

        items = ItemCarrito.objects.filter(carrito=carrito)
        for item in items:
            subtotal = item.producto.precio_venta * item.cantidad
            lista_items.append({
                'producto': item.producto,
                'cantidad': item.cantidad,
                'subtotal': subtotal,
            })
            total += subtotal

    context = {
    'items': lista_items,
    'total': total,
    }

    return render(request, 'carrito.html', context)



def eliminar_del_carrito(request, producto_id):
    # Verifica si el usuario está autenticado
    if request.user.is_authenticated:
        carrito = Carrito.objects.filter(usuario=request.user).first()
    else:
        session_key = request.session.session_key
        carrito = Carrito.objects.filter(session_key=session_key).first()

    # Si no existe el carrito
    if not carrito:
        return redirect('ver_carrito')

    # Verifica si el producto está en el carrito
    item = ItemCarrito.objects.filter(carrito=carrito, producto_id=producto_id).first()

    if item:
        item.delete()
    else:
        # Puedes agregar un mensaje de error si el producto no está en el carrito
        print(f"Producto con ID {producto_id} no encontrado en el carrito.")
    
    return redirect('ver_carrito')


def vaciar_carrito(request):
    if request.user.is_authenticated:
        carrito = Carrito.objects.filter(usuario=request.user).first()
    else:
        session_key = request.session.session_key
        carrito = Carrito.objects.filter(session_key=session_key).first()

    if carrito:
        ItemCarrito.objects.filter(carrito=carrito).delete()

    return redirect('ver_carrito')


def detalle_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    return render(request, 'detalle_producto.html', {'producto': producto})

def productos_por_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, pk=categoria_id)
    productos = Producto.objects.filter(categoria=categoria)

    return render(request, 'productos.html', {
        'categoria': categoria,
        'productos': productos
    })


@login_required
def pagar(request):
    # Verificar si el usuario tiene un carrito asociado
    carrito = Carrito.objects.filter(usuario=request.user).first()

    # Si el usuario no tiene carrito, verificar en la sesión
    if not carrito:
        # Verificar si hay un carrito en la sesión
        session_key = request.session.session_key
        if session_key:
            try:
                # Obtener el carrito asociado a la sesión
                carrito_sesion = Carrito.objects.get(session_key=session_key, usuario__isnull=True)
                
                # Crear un carrito para el usuario si no existe
                carrito, creado = Carrito.objects.get_or_create(usuario=request.user)

                # Transferir los items del carrito de sesión al carrito del usuario
                for item in ItemCarrito.objects.filter(carrito=carrito_sesion):
                    item_existente = ItemCarrito.objects.filter(carrito=carrito, producto=item.producto).first()
                    if item_existente:
                        item_existente.cantidad += item.cantidad
                        item_existente.save()
                    else:
                        item.carrito = carrito
                        item.pk = None  # Clonar el objeto
                        item.save()

                # Eliminar el carrito de la sesión
                carrito_sesion.delete()

            except Carrito.DoesNotExist:
                # Si no hay carrito en la sesión, simplemente seguimos sin carrito
                carrito = None

    if not carrito:
        return render(request, 'error.html', {'mensaje': 'No tienes productos en tu carrito.'})

    items = ItemCarrito.objects.filter(carrito=carrito)
    total = sum(item.producto.precio_venta * item.cantidad for item in items)


    # Mostrar el carrito y el total
    context = {
        'carrito': carrito,
        'items': items,
        'total': total,
    }


    return render(request, 'pagar.html', context)


