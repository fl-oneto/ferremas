from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('myaccount/', views.myaccount, name='myaccount'),
    path('editar_perfil/', views.editar_perfil, name='editar_perfil'),
    path('agregar/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('eliminar/<int:producto_id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
    path('carrito/', views.ver_carrito, name='ver_carrito'),
    path('vaciar/', views.vaciar_carrito, name='vaciar_carrito'),
    path('producto/<int:producto_id>/', views.detalle_producto, name='detalle_producto'),
    path('categoria/<int:categoria_id>/', views.productos_por_categoria, name='productos_por_categoria'),
    path('pagar/', views.pagar, name='pagar'),
    path('buscar-producto/', views.buscar_producto, name='buscar_producto'),
    path('ajax/cargar-comunas/', views.cargar_comunas, name='cargar_comunas'),
    path('completar_datos/', views.completar_datos_usuario, name='completar_datos_usuario'),
    path('confirmar_pedido/', views.confirmar_pedido, name='confirmar_pedido'),
    path('elegir_metodo_pago/', views.elegir_metodo_pago, name='elegir_metodo_pago'),
    path('procesar_pago_paypal/', views.procesar_pago_paypal, name='procesar_pago_paypal'),
    path('confirmar_pago/', views.confirmar_pago, name='confirmar_pago'),
    path('bodeguero/', views.dashboard_bodeguero, name='dashboard_bodeguero'),
    path('bodeguero/pedidos/', views.pedidos_pendientes, name='pedidos_pendientes'),
    path('bodeguero/pedido/<int:pedido_id>/', views.pedido_detalle, name='detalle_pedido'),
    path('bodeguero/preparados/', views.pedidos_preparados, name='pedidos_preparados'),
    path('redirect/', views.redirect_post_login, name='redirect_post_login'),
    path('vendedor/productos/', views.productos_disponibles, name='productos_disponibles'),
    path('vendedor/pedidos/', views.pedidos_por_aprobar, name='pedidos_por_aprobar'),
    path('vendedor/pedido/<int:pedido_id>/', views.aprobar_rechazar_pedido, name='aprobar_rechazar_pedido'),
    path('vendedor/despacho/', views.pedidos_despacho, name='pedidos_despacho'),
    path('vendedor/', views.dashboard_vendedor, name='dashboard_vendedor'),

]

