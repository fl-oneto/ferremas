from django.contrib import admin
from .models import Categoria, Producto, Region, Comuna, Direccion, Telefono, Perfil, EstadoPedido 
from .models import UnidadMedida, Carrito, ItemCarrito, Pedido, DetallePedido, MetodoPago, Pago

admin.site.register(Categoria)
admin.site.register(Producto)
admin.site.register(Region)
admin.site.register(Comuna)
admin.site.register(Direccion)
admin.site.register(Telefono)
admin.site.register(UnidadMedida)
admin.site.register(Carrito)
admin.site.register(ItemCarrito)
admin.site.register(Pedido)
admin.site.register(DetallePedido)
admin.site.register(MetodoPago)
admin.site.register(Pago)
admin.site.register(EstadoPedido)
admin.site.register(Perfil)

