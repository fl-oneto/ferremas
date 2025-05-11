from django.contrib.auth.decorators import user_passes_test

def grupo_requerido(nombre_grupo):
    """
    Decorador que restringe el acceso a usuarios que pertenezcan a un grupo específico.
    """
    def pertenece_al_grupo(user):
        return user.is_authenticated and user.groups.filter(name=nombre_grupo).exists()
    
    return user_passes_test(pertenece_al_grupo, login_url='login', redirect_field_name=None)
