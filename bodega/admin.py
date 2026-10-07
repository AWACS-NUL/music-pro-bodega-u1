from django.contrib import admin
from .models import (
    Categoria, Marca, Proveedor, ZonaBodega, UbicacionFisica,
    Producto, SucursalDestino, OrdenDespacho, DetalleDespacho, AuditoriaStock
)

modelos_bodega = [
    Categoria, Marca, Proveedor, ZonaBodega, UbicacionFisica,
    Producto, SucursalDestino, OrdenDespacho, DetalleDespacho, AuditoriaStock
]

for modelo in modelos_bodega:
    # Obtener dinámicamente los nombres de todos los campos concretos del modelo
    campos_modelo = tuple(campo.name for campo in modelo._meta.fields)
    
    # Crear una clase ModelAdmin adaptada a las columnas reales existentes
    admin_class = type(
        f"{modelo.__name__}AutoAdmin",
        (admin.ModelAdmin,),
        {
            "list_display": campos_modelo,
            "search_fields": tuple(
                campo.name for campo in modelo._meta.fields 
                if campo.get_internal_type() in ("CharField", "TextField")
            ),
        }
    )
    
    admin.site.register(modelo, admin_class)