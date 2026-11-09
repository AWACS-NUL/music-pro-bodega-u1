from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
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


# ==================== GESTIÓN DE USUARIOS ====================

class UsuarioRegistroForm(UserCreationForm):
    email = forms.EmailField(
        required=False,
        label='Correo Electrónico',
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    is_staff = forms.BooleanField(
        required=False,
        label='Perfil de Administrador (staff)',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'is_staff']
        labels = {
            'username': 'Nombre de Usuario',
            'password1': 'Contraseña',
            'password2': 'Confirmar Contraseña',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for nombre in ['username', 'password1', 'password2']:
            self.fields[nombre].widget.attrs.update({'class': 'form-control'})
            self.fields[nombre].help_text = None


class UsuarioEdicionForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'is_active', 'is_staff']
        labels = {
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'email': 'Correo Electrónico',
            'is_active': 'Usuario Activo',
            'is_staff': 'Perfil de Administrador (staff)',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for nombre, campo in self.fields.items():
            if nombre in ('is_active', 'is_staff'):
                campo.widget.attrs.update({'class': 'form-check-input'})
            else:
                campo.widget.attrs.update({'class': 'form-control'})
