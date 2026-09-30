from django.urls import path
from . import views

app_name = 'bodega'

urlpatterns = [
    path('', views.panel_inventario, name='panel'),
    path('movimiento/', views.movimiento_mercaderia, name='movimiento'),
]