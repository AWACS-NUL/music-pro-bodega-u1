from django import forms
from .models import Producto, OrdenDespacho, DetalleDespacho


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = [
            'codigo', 'nombre', 'categoria', 'marca',
            'proveedor_principal', 'ubicacion',
            'precio_unitario', 'stock_actual', 'stock_minimo',
        ]
        labels = {
            'codigo': 'Código SKU',
            'proveedor_principal': 'Proveedor Principal',
            'precio_unitario': 'Precio Unitario (CLP)',
            'stock_actual': 'Stock Actual',
            'stock_minimo': 'Stock Mínimo',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for campo in self.fields.values():
            if campo.widget.__class__.__name__ == 'Select':
                campo.widget.attrs.update({'class': 'form-select'})
            elif not isinstance(campo.widget, forms.CheckboxInput):
                campo.widget.attrs.update({'class': 'form-control'})


class OrdenDespachoForm(forms.ModelForm):
    class Meta:
        model = OrdenDespacho
        fields = ['numero_guia', 'sucursal_destino', 'estado']
        labels = {
            'numero_guia': 'Número de Guía',
            'sucursal_destino': 'Sucursal de Destino',
            'estado': 'Estado',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['sucursal_destino'].widget.attrs.update({'class': 'form-select'})
        self.fields['estado'].widget.attrs.update({'class': 'form-select'})
        self.fields['numero_guia'].widget.attrs.update({'class': 'form-control'})


class DetalleDespachoForm(forms.ModelForm):
    class Meta:
        model = DetalleDespacho
        fields = ['producto', 'cantidad_solicitada']
        labels = {
            'producto': 'Producto',
            'cantidad_solicitada': 'Cantidad',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['producto'].widget.attrs.update({'class': 'form-select'})
        self.fields['cantidad_solicitada'].widget.attrs.update({'class': 'form-control'})
