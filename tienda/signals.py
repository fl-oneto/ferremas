from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from .models import Carrito, ItemCarrito, Perfil
from django.db.models.signals import post_save
from django.contrib.auth.models import User


@receiver(user_logged_in)
def migrar_carrito_session_a_usuario(sender, request, user, **kwargs):
    session_key = request.session.session_key
    if not session_key:
        return

    try:
        carrito_sesion = Carrito.objects.get(session_key=session_key, usuario__isnull=True)
    except Carrito.DoesNotExist:
        return

    # Verificar si ya existe un carrito de usuario
    carrito_usuario, creado = Carrito.objects.get_or_create(usuario=user)

    for item in ItemCarrito.objects.filter(carrito=carrito_sesion):
        item_existente = ItemCarrito.objects.filter(carrito=carrito_usuario, producto=item.producto).first()
        if item_existente:
            item_existente.cantidad += item.cantidad
            item_existente.save()
        else:
            item.carrito = carrito_usuario
            item.pk = None  # esto clona el objeto
            item.save()

    carrito_sesion.delete()
    
@receiver(post_save, sender=User)
def crear_perfil_usuario(sender, instance, created, **kwargs):
    if created:
        Perfil.objects.create(usuario=instance)

@receiver(post_save, sender=User)
def guardar_perfil_usuario(sender, instance, **kwargs):
    instance.perfil.save()
