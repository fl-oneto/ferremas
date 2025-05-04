from django import template

register = template.Library()

@register.filter
def formatear_pesos(valor):
    try:
        valor = int(valor)
        valor_formateado = '{:,}'.format(valor).replace(',', '.')
        return f"{valor_formateado} CLP"
    except (ValueError, TypeError):
        return valor