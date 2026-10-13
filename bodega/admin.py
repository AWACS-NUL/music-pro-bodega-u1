from django.contrib import admin
from .models import (
    Categoria, Marca, Proveedor, ZonaBodega, UbicacionFisica,
    Producto, SucursalDestino, OrdenDespacho, DetalleDespacho, AuditoriaStock
)


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')
    search_fields = ('nombre', 'descripcion')
    ordering = ('nombre',)


@admin.register(Marca)
class MarcaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'pais_origen')
    search_fields = ('nombre', 'pais_origen')
    ordering = ('nombre',)


@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ('rut', 'razon_social', 'contacto_email', 'telefono')
    search_fields = ('rut', 'razon_social', 'contacto_email')
    list_filter = ('razon_social',)
    ordering = ('razon_social',)


@admin.register(ZonaBodega)
class ZonaBodegaAdmin(admin.ModelAdmin):
    list_display = ('codigo_zona', 'nombre', 'temperatura_controlada')
    search_fields = ('codigo_zona', 'nombre')
    list_filter = ('temperatura_controlada',)
    ordering = ('codigo_zona',)


@admin.register(UbicacionFisica)
class UbicacionFisicaAdmin(admin.ModelAdmin):
    list_display = ('zona', 'pasillo', 'estante', 'nivel')
    search_fields = ('pasillo', 'estante', 'nivel')
    list_filter = ('zona',)
    ordering = ('zona', 'pasillo', 'estante', 'nivel')


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre', 'categoria', 'marca', 'stock_actual', 'stock_minimo', 'precio_unitario')
    search_fields = ('codigo', 'nombre')
    list_filter = ('categoria', 'marca', 'proveedor_principal')
    ordering = ('codigo',)


@admin.register(SucursalDestino)
class SucursalDestinoAdmin(admin.ModelAdmin):
    list_display = ('codigo_sucursal', 'nombre', 'direccion', 'ciudad')
    search_fields = ('codigo_sucursal', 'nombre', 'direccion', 'ciudad')
    list_filter = ('ciudad',)
    ordering = ('codigo_sucursal',)


@admin.register(OrdenDespacho)
class OrdenDespachoAdmin(admin.ModelAdmin):
    list_display = ('numero_guia', 'sucursal_destino', 'estado', 'fecha_creacion')
    search_fields = ('numero_guia',)
    list_filter = ('estado', 'sucursal_destino', 'fecha_creacion')
    ordering = ('-fecha_creacion',)


@admin.register(DetalleDespacho)
class DetalleDespachoAdmin(admin.ModelAdmin):
    list_display = ('orden', 'producto', 'cantidad_solicitada')
    search_fields = ('orden__numero_guia', 'producto__codigo', 'producto__nombre')
    list_filter = ('orden',)
    ordering = ('orden',)


@admin.register(AuditoriaStock)
class AuditoriaStockAdmin(admin.ModelAdmin):
    list_display = ('producto', 'tipo_ajuste', 'cantidad_afectada', 'fecha_auditoria')
    search_fields = ('producto__codigo', 'producto__nombre', 'observacion')
    list_filter = ('tipo_ajuste', 'fecha_auditoria')
    ordering = ('-fecha_auditoria',)