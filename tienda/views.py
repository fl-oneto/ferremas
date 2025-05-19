from django.urls import reverse
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from .models import Categoria, Producto, Region, Comuna, Direccion, Telefono, UnidadMedida, Carrito, ItemCarrito, Pedido, DetallePedido, EstadoPedido, MetodoPago, Pago, Perfil
from django.contrib.auth import login
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .forms import ClienteCreationForm, DatosUsuarioForm, EmailLoginForm, TrabajadorCreationForm, ProductoForm, CategoriaForm
from django.contrib.auth.decorators import login_required
import requests
from django.conf import settings
from .utils import clp_a_usd
from .decorators import grupo_requerido
from django.utils.http import url_has_allowed_host_and_scheme
from django.contrib import messages
from datetime import date, timedelta
from django.db.models import Sum




@login_required
def redirect_post_login(request):
    user = request.user
    if user.groups.filter(name='Bodeguero').exists():
        return redirect('dashboard_bodeguero') 
    elif user.groups.filter(name='Vendedor').exists():
        return redirect('dashboard_vendedor')
    elif user.groups.filter(name='Administrador').exists():
        return redirect('dashboard_admin')  
    elif user.groups.filter(name='Contador').exists():
        return redirect('dashboard_contador')  
    elif user.groups.filter(name='Cliente').exists():
        return redirect('home')  # O la página de productos
    else:
        return redirect('home')  # Fallback por si no tiene grupo

#lógica de registro e inicio de sesión

def login_view(request):
    if request.method == 'POST':
        form = EmailLoginForm(request.POST)
        if form.is_valid():
            login(request, form.user)
            next_url = request.POST.get('next')
            if next_url and url_has_allowed_host_and_scheme(next_url, request.get_host()):
                return redirect(next_url)
            return redirect('redirect_post_login')
    else:
        form = EmailLoginForm()
    return render(request, 'registro/login.html', {'form': form})


def signup(request):
    if request.method == 'POST':
        form = ClienteCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            grupo_cliente = Group.objects.get(name='Cliente')
            user.groups.add(grupo_cliente)
            login(request, user)  
            return redirect('login') 
    else:
        form = ClienteCreationForm()
    return render(request, 'registro/signup.html', {'form': form})


def home(request):
    if request.user.is_authenticated:
        if request.user.groups.filter(name='Administrador').exists():
            return redirect('dashboard_admin')
        elif request.user.groups.filter(name='Vendedor').exists():
            return redirect('dashboard_vendedor')
        elif request.user.groups.filter(name='Bodeguero').exists():
            return redirect('dashboard_bodeguero')
        elif request.user.groups.filter(name='Contador').exists():
            return redirect('dashboard_contador')
        
    categorias = (
        Categoria.objects
        .prefetch_related('producto_set') 
        .order_by('nombre')
    )
    productos = Producto.objects.all()

    context = {
        'categorias': categorias,
        'productos': productos,
     }
    
    return render(request, 'home.html', context)

def acceso_denegado(request):
    return render(request, 'acceso_denegado.html', status=403)

def about(request):
    return render(request, 'core/about.html')

def faq(request):
    return render(request, 'core/faq.html')

def joinus(request):
    return render(request, 'core/joinus.html')

def contact(request):
    return render(request, 'core/contact.html')

@login_required
def myaccount(request):
    usuario = request.user
    telefono = Telefono.objects.filter(usuario=usuario).first()
    direccion = Direccion.objects.filter(usuario=usuario).first()
    pedidos = Pedido.objects.filter(cliente=usuario).order_by('-fecha')

    return render(request, 'registro/myaccount.html', {
        'usuario': usuario,
        'telefono': telefono,
        'direccion': direccion,
        'pedidos': pedidos,
    })

#lógica y CRUD del carrito 

def agregar_al_carrito(request, producto_id):
    print("POST data:", request.POST)

    producto = get_object_or_404(Producto, pk=producto_id)
    cantidad = int(request.POST.get('cantidad', 1))

    
    if cantidad > producto.stock:
        return render(request, 'error_stock.html', {'mensaje': 'No hay suficiente stock disponible.'})


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

#lógica de productos

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
    
@grupo_requerido('Cliente')
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


def buscar_producto(request):
    q = request.GET.get('q', '')
    resultados = Producto.objects.filter(nombre__icontains=q).values('id', 'nombre')[:10]
    return JsonResponse(list(resultados), safe=False)

#comunas

def cargar_comunas(request):
    region_id = request.GET.get('region')
    print("Region ID recibido:", region_id)
    comunas = Comuna.objects.filter(region_id=region_id).values('id', 'nombre')
    print("Comunas encontradas:", list(comunas))
    return JsonResponse(list(comunas), safe=False)

#lógica perfil de usuario

@login_required
def editar_perfil(request):
    return procesar_formulario_usuario(
        request,
        redireccion='myaccount',
        titulo='Editar perfil',
        boton='Guardar cambios'
    )

@login_required
def completar_datos_usuario(request):
    return procesar_formulario_usuario(
        request,
        redireccion='confirmar_pedido',
        titulo='Confirma tus datos antes de continuar con el pedido',
        boton='Confirmar y continuar'
    )
@login_required
def procesar_formulario_usuario(request, redireccion, titulo, boton):
    usuario = request.user
    telefono = Telefono.objects.filter(usuario=usuario).first()
    direccion = Direccion.objects.filter(usuario=usuario).first()
    regiones = Region.objects.all()

    region_id = None
    if request.method == 'POST':
        region_id = request.POST.get('region')
        form = DatosUsuarioForm(request.POST, region_id=region_id)
        if form.is_valid():
            # Guardar datos del perfil
            usuario.perfil.nombre = form.cleaned_data['nombre']
            usuario.perfil.primer_apellido = form.cleaned_data['primer_apellido']
            usuario.perfil.segundo_apellido = form.cleaned_data.get('segundo_apellido', '')
            usuario.perfil.save()

            Telefono.objects.update_or_create(
                usuario=usuario,
                defaults={'numero': form.cleaned_data['telefono']}
            )

            Direccion.objects.update_or_create(
                usuario=usuario,
                defaults={
                    'calle': form.cleaned_data['calle'],
                    'numero': form.cleaned_data['numero'],
                    'comuna': form.cleaned_data['comuna'],
                    'codigo_postal': None
                }
            )

            return redirect(redireccion)
    else:
        initial_data = {
            'nombre': usuario.perfil.nombre if hasattr(usuario, 'perfil') else '',
            'primer_apellido': usuario.perfil.primer_apellido if hasattr(usuario, 'perfil') else '',
            'segundo_apellido': usuario.perfil.segundo_apellido if hasattr(usuario, 'perfil') else '',
            'telefono': telefono.numero if telefono else '',
            'calle': direccion.calle if direccion else '',
            'numero': direccion.numero if direccion else '',
            'region': direccion.comuna.region if direccion and direccion.comuna else None,
            'comuna': direccion.comuna if direccion else None,
        }
        region_id = direccion.comuna.region.id if direccion and direccion.comuna else None
        form = DatosUsuarioForm(initial=initial_data, region_id=region_id)

    return render(request, 'registro/editar_perfil.html', {
        'form': form,
        'regiones': regiones,
        'telefono': telefono,
        'direccion': direccion,
        'titulo': titulo,
        'texto_boton': boton,
    })
    
#validar stock
def validar_stock(items):
    errores = []
    for item in items:
        if item.cantidad > item.producto.stock:
            errores.append(
                f"No hay suficiente stock para '{item.producto.nombre}'. Solo hay {item.producto.stock} disponibles."
            )
    return errores
 
    
#lógica de pedidos    
@grupo_requerido('Cliente')
def confirmar_pedido(request):
    usuario = request.user
    carrito = Carrito.objects.filter(usuario=usuario).first()
    items_qs = ItemCarrito.objects.filter(carrito=carrito)

    if not carrito or not items_qs.exists():
        return redirect('carrito')

    errores = validar_stock(items_qs)
    if errores:
        for error in errores:
            messages.error(request, error)
        return redirect('carrito')

    items = []
    total = 0
    for it in items_qs.select_related('producto'):
        subtotal = it.producto.precio_venta * it.cantidad
        items.append({
            'producto':  it.producto,
            'cantidad':  it.cantidad,
            'subtotal':  subtotal,
        })
        total += subtotal

    return render(request, 'pedido/confirmar_pedido.html', {
        'items': items,  
        'total': total,
    })

# elegir método de pago      
@grupo_requerido('Cliente')
def elegir_metodo_pago(request):
    if request.method == 'POST':
        # aca manejar otros metodos de pago
        return redirect('procesar_pago_paypal')
    
    return render(request, 'pedido/elegir_metodo_pago.html')

# integración con API de PayPal
def obtener_token_paypal():
    url = f"{settings.PAYPAL_API_BASE}/v1/oauth2/token"
    headers = {
        "Accept": "application/json",
        "Accept-Language": "es_CL",
    }
    data = {
        "grant_type": "client_credentials"
    }

    try:
        response = requests.post(url, headers=headers, data=data,
                                 auth=(settings.PAYPAL_CLIENT_ID, settings.PAYPAL_CLIENT_SECRET))

        if response.status_code == 200:
            return response.json().get("access_token")
        else:
            print(f"Error al obtener token de PayPal: {response.status_code} - {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Excepción al hacer la solicitud a PayPal: {e}")
        return None


def crear_pago(access_token, total_amount, currency='USD',
               return_url='http://localhost:8000/confirmar_pago/',
               cancel_url='http://localhost:8000/cancelar_pago/', direccion=None):
    url = f"{settings.PAYPAL_API_BASE}/v2/checkout/orders"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    amt = str(int(total_amount)) if currency == 'CLP' else f"{total_amount:.2f}"
    
    shipping_block = {}
    if direccion:
        shipping_block = {
            "shipping": {
                "name": {
                    "full_name": f"{direccion.usuario.perfil.nombre} {direccion.usuario.perfil.primer_apellido}"
                },
                "address": {
                    "address_line_1": f"{direccion.calle} {direccion.numero}",
                    "admin_area_2": direccion.comuna.nombre,
                    "admin_area_1": direccion.comuna.region.nombre,
                    "postal_code": direccion.codigo_postal or "",
                    "country_code": "CL"
                }
            }
        }
    
    body = {
        "intent": "CAPTURE",
        "purchase_units": [{
            "amount": {
                "currency_code": currency,
                "value": amt
            },
            **shipping_block
        }],
        "application_context": {
            "return_url": return_url,
            "cancel_url": cancel_url,
            "shipping_preference": "SET_PROVIDED_ADDRESS"
        }
    }

    response = requests.post(url, headers=headers, json=body)
    print("Respuesta de PayPal:", response.text)
    response.raise_for_status()
    data = response.json()

    # Extraemos correctamente el link con rel == "approve"
    approval_url = next(
        (link["href"] for link in data.get("links", []) if link.get("rel") == "approve"),
        None
    )

    return data.get("id"), approval_url


def procesar_pago_paypal(request):
    direccion = Direccion.objects.filter(usuario=request.user).first()
    usuario = request.user
    carrito = Carrito.objects.filter(usuario=usuario).first()
    items = ItemCarrito.objects.filter(carrito=carrito)

    if not carrito or not items.exists():
        return redirect('carrito')

    total = sum(item.producto.precio_venta * item.cantidad for item in items)
    try:
        total_usd = clp_a_usd(total, settings.EXCHANGERATE_API_KEY)
        print(f"Total CLP: {total} => Total USD: {total_usd}")
    except Exception as e:
        print("Error en conversión CLP a USD:", e)
        return HttpResponse("Error al convertir moneda", status=500)

    access_token = obtener_token_paypal()
    print("TOKEN:", access_token)

    order_id, approval_url = crear_pago(
        access_token,
        total_amount=total_usd,
        currency='USD',  # o la moneda que estés usando en sandbox
        return_url=request.build_absolute_uri('/confirmar_pago/'),
        cancel_url=request.build_absolute_uri('/cancelar_pago/'),
        direccion=direccion
    )

    if not approval_url:
        # Si algo falló, muestra un error
        print("error de approval_url:", approval_url)

        return render(request, 'pedido/error_pago.html', {'error': 'No se pudo iniciar la orden en PayPal.'})

    # Guardar order_id si lo necesitas:
    request.session['paypal_order_id'] = order_id

    # 🛫 Redirigir al usuario al approval_url de PayPal
    print("APPROVAL URL:", approval_url)
    print("TYPE:", type(approval_url))

    return redirect(approval_url)

def confirmar_pago(request):
    order_id = request.GET.get('token')
    access_token = obtener_token_paypal()
    url = f"{settings.PAYPAL_API_BASE}/v2/checkout/orders/{order_id}/capture"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.post(url, headers=headers)
    print("RESPUESTA PAYPAL:", response.status_code, response.text)
    
    if response.status_code == 201:
        datos_pago = response.json()
        # traer datos de usuario
        usuario = request.user
        carrito = Carrito.objects.filter(usuario=usuario).first()
        items = ItemCarrito.objects.filter(carrito=carrito)

        if not carrito or not items.exists():
            return render(request, 'pedido/error_pago.html', {'error': 'No hay productos en el carrito.'})
        
        # crear el pedido
        estado_pendiente, _ = EstadoPedido.objects.get_or_create(nombre="Pendiente")
        total = sum(item.producto.precio_venta * item.cantidad for item in items)
        pedido = Pedido.objects.create(
            cliente=usuario,
            estado=estado_pendiente,
            total=total
        )
        
        #detalle del pedido
        for item in items:
            DetallePedido.objects.create(
                pedido=pedido,
                producto=item.producto,
                cantidad=item.cantidad,
                precio_unitario=item.producto.precio_venta
            )
            producto = item.producto
            producto.stock -= item.cantidad
            producto.save()
        
        # guardar metodo de pago
        metodo_paypal, _ = MetodoPago.objects.get_or_create(nombre="PayPal", defaults={"descripcion": "Pago a través de PayPal"})

        # guardar pago
        Pago.objects.create(
            pedido=pedido,
            metodo_pago=metodo_paypal,
            estado="Completado",
            fecha_pago=timezone.now()
        )
        # vaciar carrito
        items.delete()
        carrito.delete()
        
        return render(request, 'pedido/pago_exitoso.html', {
            'monto': datos_pago['purchase_units'][0]['payments']['captures'][0]['amount']['value'],
            'moneda': datos_pago['purchase_units'][0]['payments']['captures'][0]['amount']['currency_code'],
            'email': datos_pago['payer']['email_address'],
            'nombre': datos_pago['payer']['name']['given_name'] + " " + datos_pago['payer']['name']['surname']
        })
    else:
        return render(request, 'pedido/error_pago.html', {'error': response.text})
    
@grupo_requerido('Cliente')
def cancelar_pago(request):
    return render(request, 'pedido/cancelar_pago.html')

# lógica de vista de bodeguero

@grupo_requerido('Bodeguero')
def dashboard_bodeguero(request):
    
    pedidos_preparacion = Pedido.objects.filter(estado='3').count()
    pedidos_listos = Pedido.objects.filter(estado='4').count()
    context = {
        'pedidos_preparacion': pedidos_preparacion,
        'pedidos_listos': pedidos_listos,
    }
    return render(request, 'pedido/bodeguero/dashboard.html', context)

@grupo_requerido('Bodeguero')
def pedidos_pendientes(request):
    estado_preparando = EstadoPedido.objects.get(nombre="En preparación")
    pedidos = Pedido.objects.filter(estado=estado_preparando)
    return render(request, 'pedido/bodeguero/pedidos_pendientes.html', {'pedidos': pedidos})

@grupo_requerido('Bodeguero')
def pedido_detalle(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    if request.method == 'POST':
        accion = request.POST.get('accion')
        if accion == 'listo':
            estado_listo = EstadoPedido.objects.get(nombre="Listo para despacho")
            pedido.estado = estado_listo
        pedido.save()
        return redirect('pedidos_pendientes')
    return render(request, 'pedido/bodeguero/detalle_pedido.html', {'pedido': pedido})

@grupo_requerido('Bodeguero')
def pedidos_preparados(request):
    estado_preparado = EstadoPedido.objects.get(nombre="Listo para despacho")
    pedidos = Pedido.objects.filter(estado=estado_preparado)
    return render(request, 'pedido/bodeguero/pedidos_preparados.html', {'pedidos': pedidos})

#vista del vendedor
@grupo_requerido('Vendedor')
def productos_disponibles(request):
    productos = Producto.objects.filter(stock__gt=0)
    return render(request, 'pedido/vendedor/productos_disponibles.html', {'productos': productos})

@grupo_requerido('Vendedor')
def pedidos_por_aprobar(request):
    estado_pendiente = EstadoPedido.objects.get(nombre="Pendiente")
    pedidos = Pedido.objects.filter(estado=estado_pendiente)
    return render(request, 'pedido/vendedor/pedidos_por_aprobar.html', {'pedidos': pedidos})

@grupo_requerido('Vendedor')
def aprobar_rechazar_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    if request.method == 'POST':
        accion = request.POST.get('accion')
        if accion == 'aprobar':
            estado_preparando = EstadoPedido.objects.get(nombre="En preparación")
            pedido.estado = estado_preparando
        elif accion == 'rechazar':
            estado_cancelado = EstadoPedido.objects.get(nombre="Cancelado")
            pedido.estado = estado_cancelado
        pedido.save()
        return redirect('pedidos_por_aprobar')
    return render(request, 'pedido/vendedor/detalle_pedido.html', {'pedido': pedido})

@grupo_requerido('Vendedor')
def pedidos_despacho(request):
    estado_preparado = EstadoPedido.objects.get(nombre="Listo para despacho")
    pedidos = Pedido.objects.filter(estado=estado_preparado)

    return render(request, 'pedido/vendedor/pedidos_despacho.html', {'pedidos': pedidos})

@grupo_requerido('Vendedor')
def despachar_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    
    estado_despachado = EstadoPedido.objects.get(nombre="Despachado")
    pedido.estado = estado_despachado
    pedido.save()

    messages.success(request, f"El pedido #{pedido.id} ha sido despachado.")

    return redirect('pedidos_despacho')

@grupo_requerido('Vendedor')
def dashboard_vendedor(request):
    pedidos_pendientes  = Pedido.objects.filter(estado='2').count()
    pedidos_despachados = Pedido.objects.filter(estado='4').count()

    today      = date.today()
    yesterday  = today - timedelta(days=1)
    day_before = today - timedelta(days=2)

    total_today = (Pedido.objects
                   .filter(fecha=today)
                   .aggregate(total=Sum('total'))['total'] or 0)

    total_yesterday = (Pedido.objects
                       .filter(fecha=yesterday)
                       .aggregate(total=Sum('total'))['total'] or 0)

    total_before = (Pedido.objects
                    .filter(fecha=day_before)
                    .aggregate(total=Sum('total'))['total'] or 0)


    context = {
        'pedidos_pendientes':  pedidos_pendientes,
        'pedidos_despachados': pedidos_despachados,


        'labels': [
            day_before.strftime('%a %d %b'),   # p. ej. "Fri 16 May"
            yesterday.strftime('%a %d %b'),
            today.strftime('%a %d %b')
        ],
        'amounts': [
            total_before,
            total_yesterday,
            total_today
        ],

        'money_two_days_ago': total_before,
        'money_yesterday':    total_yesterday,
        'money_today':        total_today,
    }

    return render(request, 'pedido/vendedor/dashboard.html', context)


#lógica del administrador

@grupo_requerido('Administrador')
def dashboard_admin(request):
    pedidos_pendientes   = Pedido.objects.filter(estado='2').count()
    pedidos_despachados  = Pedido.objects.filter(estado='5').count()
    pedidos_preparacion  = Pedido.objects.filter(estado='3').count()
    pedidos_listos       = Pedido.objects.filter(estado='4').count()

    today       = date.today()
    yesterday   = today - timedelta(days=1)
    day_before  = today - timedelta(days=2)

    total_today = (Pedido.objects
                   .filter(fecha=today)
                   .aggregate(total=Sum('total'))['total'] or 0)

    total_yesterday = (Pedido.objects
                       .filter(fecha=yesterday)
                       .aggregate(total=Sum('total'))['total'] or 0)

    total_before = (Pedido.objects
                    .filter(fecha=day_before)
                    .aggregate(total=Sum('total'))['total'] or 0)

    context = {
        'pedidos_pendientes':  pedidos_pendientes,
        'pedidos_despachados': pedidos_despachados,

        'pedidos_preparacion': pedidos_preparacion,
        'pedidos_listos':      pedidos_listos,


        'labels': [
            day_before.strftime('%a %d %b'),
            yesterday.strftime('%a %d %b'),
            today.strftime('%a %d %b')
        ],
        'amounts': [
            total_before,
            total_yesterday,
            total_today
        ],

        'money_two_days_ago': total_before,
        'money_yesterday':    total_yesterday,
        'money_today':        total_today,
    }

    return render(request, 'panel_admin/dashboard.html', context)

# gestión usuarios
@grupo_requerido('Administrador')
def gestion_usuarios(request):
    usuarios = User.objects.all()
    return render(request, 'panel_admin/gestion_usuarios.html', {'usuarios': usuarios})

@grupo_requerido('Administrador')
def crear_usuario(request):
    if request.method == 'POST':
        form = TrabajadorCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('gestion_usuarios')
    else:
        form = TrabajadorCreationForm()
    return render(request, 'panel_admin/form_usuario.html', {'form': form})

@grupo_requerido('Administrador')
def editar_usuario(request, usuario_id):
    usuario = User.objects.get(id=usuario_id)
    if request.method == 'POST':
        form = TrabajadorCreationForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            return redirect('gestion_usuarios')
    else:
        form = TrabajadorCreationForm(instance=usuario)
    return render(request, 'panel_admin/form_usuario.html', {'form': form})

@grupo_requerido('Administrador')
def eliminar_usuario(request, usuario_id):
    usuario = get_object_or_404(User, id=usuario_id)
    usuario.delete()
    return redirect('gestion_usuarios')

#crud categorias gestion admin
@grupo_requerido('Administrador')
def gestion_categorias(request):
    categorias = Categoria.objects.all()
    return render(request, 'panel_admin/gestion_categorias.html', {'categorias': categorias})

@grupo_requerido('Administrador')
def crear_categoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoría creada correctamente.')
            return redirect('gestion_categorias')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        form = CategoriaForm()

    contexto = {
        'form': form,
        'titulo': 'Agregar Categoría',
        'texto_boton': 'Crear Categoría',
        'url_volver': reverse('gestion_categorias'),
    }
    return render(request, 'panel_admin/form_gestion.html', contexto)

@grupo_requerido('Administrador')
def editar_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)
    if request.method == 'POST':
        form = CategoriaForm(request.POST, request.FILES, instance=categoria)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoría actualizada correctamente.')
            return redirect('gestion_categorias')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        form = CategoriaForm(instance=categoria)

    contexto = {
        'form': form,
        'titulo': 'Editar Categoría',
        'texto_boton': 'Actualizar Categoría',
        "url_volver": reverse("gestion_categorias"),
    }
    return render(request, 'panel_admin/form_gestion.html', contexto)

@grupo_requerido('Administrador')
def eliminar_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)
    if request.method == 'POST':
        categoria.delete()
        messages.success(request, 'Categoría eliminada correctamente.')
        return redirect('gestion_categorias')
    return render(request, 'panel_admin/confirmar_eliminacion_categoria.html', {'categoria': categoria})


# crud productos gestion admin

@grupo_requerido('Administrador')
def gestion_productos(request):
    productos = Producto.objects.all()
    return render(request, 'panel_admin/gestion_productos.html', {'productos': productos})

@grupo_requerido('Administrador')
def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            producto = form.save(commit=False)
            producto.categoria = form.cleaned_data["categoria"]
            producto.save()
            messages.success(request, f'Producto “{producto.nombre}” agregado correctamente.')
            return redirect('gestion_productos')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        form = ProductoForm()

    contexto = {
        'form': form,
        'titulo': 'Agregar producto',
        'texto_boton': 'Crear Producto',
        'url_volver': reverse('gestion_productos'),
    }
    return render(request, 'panel_admin/form_gestion.html', contexto)


@grupo_requerido('Administrador')
def editar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('gestion_productos')
    else:
        form = ProductoForm(instance=producto)
    contexto = {
        'form': form,
        'titulo': 'Editar producto',          
        'texto_boton': 'Guardar cambios',     
         "url_volver": reverse("gestion_productos"),
    }
    return render(request, 'panel_admin/form_gestion.html', contexto)

@grupo_requerido('Administrador')
def eliminar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    producto.delete()
    return redirect('gestion_productos')

#logica contador

@grupo_requerido('Contador')
def dashboard_contador(request):
    today       = date.today()
    yesterday   = today - timedelta(days=1)
    day_before  = today - timedelta(days=2)

    total_today = (Pedido.objects
                   .filter(fecha=today)
                   .aggregate(total=Sum('total'))['total'] or 0)

    total_yesterday = (Pedido.objects
                       .filter(fecha=yesterday)
                       .aggregate(total=Sum('total'))['total'] or 0)

    total_before = (Pedido.objects
                    .filter(fecha=day_before)
                    .aggregate(total=Sum('total'))['total'] or 0)

    context = {
        'labels': [
            day_before.strftime('%a %d %b'),
            yesterday.strftime('%a %d %b'),
            today.strftime('%a %d %b')
        ],
        'amounts': [
            total_before,
            total_yesterday,
            total_today
        ],

        'money_two_days_ago': total_before,
        'money_yesterday':    total_yesterday,
        'money_today':        total_today,
    }
    return render(request, 'pedido/contador/dashboard.html', context)

@grupo_requerido('Contador')
def listar_pagos(request):
    pagos = Pago.objects.select_related('metodo_pago').all().order_by('-fecha_pago')
    context = {
        'pagos': pagos,
    }
    return render(request, 'pedido/contador/pagos.html', context)