from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    
    # -- urls de registro y autenticacion --
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('acceso-denegado/', views.acceso_denegado, name='acceso_denegado'),
    path('myaccount/', views.myaccount, name='myaccount'),
    path('editar_perfil/', views.editar_perfil, name='editar_perfil'),
    
    # -- urls recuperación de contraseña --
    path(
        "password-reset/",
        auth_views.PasswordResetView.as_view(
            template_name="registro/password_reset_form.html",
            email_template_name="registro/password_reset_email.html",
            subject_template_name="registro/password_reset_subject.txt",
            success_url="done/",
        ),
        name="password_reset",
    ),
    path(
        "password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="registro/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="registro/password_reset_confirm.html",
            success_url="/reset/done/",
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="registro/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
    
    # -- urls de carrito --
    path('agregar/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('eliminar/<int:producto_id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
    path('carrito/', views.ver_carrito, name='ver_carrito'),
    path('vaciar/', views.vaciar_carrito, name='vaciar_carrito'),
    
    # -- urls de productos --
    path('producto/<int:producto_id>/', views.detalle_producto, name='detalle_producto'),
    path('categoria/<int:categoria_id>/', views.productos_por_categoria, name='productos_por_categoria'),
    path('pagar/', views.pagar, name='pagar'),
    path('buscar-producto/', views.buscar_producto, name='buscar_producto'),
    path('ajax/cargar-comunas/', views.cargar_comunas, name='cargar_comunas'),
    path('completar_datos/', views.completar_datos_usuario, name='completar_datos_usuario'),
    
    # -- urls de pedidos --
    path('confirmar_pedido/', views.confirmar_pedido, name='confirmar_pedido'),
    path('elegir_metodo_pago/', views.elegir_metodo_pago, name='elegir_metodo_pago'),
    path('procesar_pago_paypal/', views.procesar_pago_paypal, name='procesar_pago_paypal'),
    path('confirmar_pago/', views.confirmar_pago, name='confirmar_pago'),
    path('cancelar_pago/', views.cancelar_pago, name='cancelar_pago'),
    
    # -- urls bodeguero -
    path('bodeguero/', views.dashboard_bodeguero, name='dashboard_bodeguero'),
    path('bodeguero/pedidos/', views.pedidos_pendientes, name='pedidos_pendientes'),
    path('bodeguero/pedido/<int:pedido_id>/', views.pedido_detalle, name='detalle_pedido'),
    path('bodeguero/preparados/', views.pedidos_preparados, name='pedidos_preparados'),
    path('redirect/', views.redirect_post_login, name='redirect_post_login'),
    
    #-- urls vendedor --
    path('vendedor/productos/', views.productos_disponibles, name='productos_disponibles'),
    path('vendedor/pedidos/', views.pedidos_por_aprobar, name='pedidos_por_aprobar'),
    path('vendedor/pedido/<int:pedido_id>/', views.aprobar_rechazar_pedido, name='aprobar_rechazar_pedido'),
    path('vendedor/despacho/', views.pedidos_despacho, name='pedidos_despacho'),
    path('pedido/<int:pedido_id>/despachar/', views.despachar_pedido, name='despachar_pedido'),
    path('vendedor/', views.dashboard_vendedor, name='dashboard_vendedor'),
    
    #-- links de informacion --
    path('about/', views.about, name='about'),
    path('faq/', views.faq, name='faq'),
    path('contact/', views.contact, name='contact'),
    path('joinus/', views.joinus, name='joinus'),
    
    #-- urls admin --
    path('administrador/', views.dashboard_admin, name='dashboard_admin'),
    path('administrador/usuarios/', views.gestion_usuarios, name='gestion_usuarios'),
    path('administrador/usuarios/crear/', views.crear_usuario, name='crear_usuario'),
    path('administrador/usuarios/<int:usuario_id>/editar/', views.editar_usuario, name='editar_usuario'),
    path('administrador/usuarios/<int:usuario_id>/eliminar/', views.eliminar_usuario, name='eliminar_usuario'),
    path('administrador/categorias/', views.gestion_categorias, name='gestion_categorias'),
    path('administrador/categorias/crear/', views.crear_categoria, name='crear_categoria'),
    path('administrador/categorias/<int:categoria_id>/editar/', views.editar_categoria, name='editar_categoria'),
    path('administrador/categorias/<int:categoria_id>/eliminar/', views.eliminar_categoria, name='eliminar_categoria'),
    path('administrador/productos/', views.gestion_productos, name='gestion_productos'),
    path('administrador/productos/crear/', views.crear_producto, name='crear_producto'),
    path('administrador/productos/<int:producto_id>/editar/', views.editar_producto, name='editar_producto'),
    path('administrador/productos/<int:producto_id>/eliminar/', views.eliminar_producto, name='eliminar_producto'),
    
    #-- urls contador --
    path('contador/', views.dashboard_contador, name='dashboard_contador'),
    path('pagos/', views.listar_pagos, name='listar_pagos'),

]

