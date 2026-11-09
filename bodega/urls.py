from django.urls import path
from . import views

app_name = 'bodega'

urlpatterns = [
    path('', views.panel_inventario, name='panel'),
    path('movimiento/', views.movimiento_mercaderia, name='movimiento'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # CRUD Productos
    path('productos/', views.producto_lista, name='producto_lista'),
    path('productos/crear/', views.producto_crear, name='producto_crear'),
    path('productos/<int:pk>/editar/', views.producto_editar, name='producto_editar'),
    path('productos/<int:pk>/eliminar/', views.producto_eliminar, name='producto_eliminar'),

    # CRUD Despachos
    path('despachos/', views.despacho_lista, name='despacho_lista'),
    path('despachos/crear/', views.despacho_crear, name='despacho_crear'),
    path('despachos/<int:pk>/', views.despacho_detalle, name='despacho_detalle'),
]
