from django.shortcuts import get_object_or_404
from .models import Categoria, Region, Comuna

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