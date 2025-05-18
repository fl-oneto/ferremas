from django.shortcuts import redirect
from django.urls import reverse
from functools import wraps

def grupo_requerido(nombre_grupo):
    """
    Decorador que restringe el acceso a usuarios que pertenezcan a un grupo específico.
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect(f"{reverse('login')}?next={request.path}")
            if not request.user.groups.filter(name=nombre_grupo).exists():
                return redirect('acceso_denegado')
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator