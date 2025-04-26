from django.contrib import admin
from .models import Categoria, Producto, Rol, Usuario, Region, Comuna, Direccion, Telefono

admin.site.register(Categoria)
admin.site.register(Producto)
admin.site.register(Rol)
admin.site.register(Usuario)
admin.site.register(Region)
admin.site.register(Comuna)
admin.site.register(Direccion)
admin.site.register(Telefono)