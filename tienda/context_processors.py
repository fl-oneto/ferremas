from django.shortcuts import get_object_or_404
from .models import Categoria, Region, Comuna
from django.urls import reverse


def categorias_disponibles(request):
    return {'categorias': Categoria.objects.all()}

def regiones_comunas(request):
    regiones = Region.objects.all()
    
    regiones_comunas = {}
    for region in regiones:
        regiones_comunas[region.nombre] = Comuna.objects.filter(region=region).order_by('nombre')

    return {
        'regiones_comunas': regiones_comunas
    }


def url_logo(request):
    if request.user.is_authenticated:
        if request.user.groups.filter(name='Bodeguero').exists():
            return {'url_logo': reverse('dashboard_bodeguero')}
        elif request.user.groups.filter(name='Vendedor').exists():
            return {'url_logo': reverse('dashboard_vendedor')}
    return {'url_logo': reverse('home')}