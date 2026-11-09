import json
from pathlib import Path
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.utils.http import url_has_allowed_host_and_scheme
from django.forms import inlineformset_factory
from django.db.models import Q, Count
from django.core.paginator import Paginator
from .models import Producto, Categoria, OrdenDespacho, DetalleDespacho
from .forms import ProductoForm, OrdenDespachoForm, DetalleDespachoForm, UsuarioRegistroForm, UsuarioEdicionForm

staff_required = user_passes_test(lambda u: u.is_staff, login_url='bodega:producto_lista')

DATA_FILE = Path(__file__).resolve().parent / 'data' / 'productos.json'

def _cargar_productos():
    if not DATA_FILE.exists():
        return []
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def _guardar_productos(productos):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(productos, f, indent=2, ensure_ascii=False)

def panel_inventario(request):
    productos = _cargar_productos()
    
    categoria_filtro = request.GET.get('categoria', '').strip()
    busqueda = request.GET.get('q', '').strip().lower()

    if categoria_filtro:
        productos = [p for p in productos if p['categoria'].lower() == categoria_filtro.lower()]

    if busqueda:
        productos = [
            p for p in productos 
            if busqueda in p['nombre'].lower() or busqueda in p['codigo'].lower()
        ]

    total_unidades = sum(p['stock_actual'] for p in productos)
    productos_criticos = [p for p in productos if p['stock_actual'] <= p['stock_minimo']]

    contexto = {
        'modulo': 'Bodega Central - Music Pro Tour 2026',
        'productos': productos,
        'total_items': len(productos),
        'total_unidades': total_unidades,
        'total_criticos': len(productos_criticos),
        'busqueda': busqueda,
        'categoria_filtro': categoria_filtro,
    }
    return render(request, 'bodega/inventario.html', contexto)

def movimiento_mercaderia(request):
    productos = _cargar_productos()
    sucursales = [
        'Sucursal Providencia (Rock)',
        'Sucursal Centro (DJ & Electrónica)',
        'Sucursal Bellavista (Cumbia & Reggaetón)',
        'Franquicia Viña del Mar'
    ]

    if request.method == 'POST':
        producto_id = request.POST.get('producto_id')
        tipo_movimiento = request.POST.get('tipo_movimiento')
        cantidad_str = request.POST.get('cantidad', '0')
        destino = request.POST.get('destino')

        # Validaciones de integridad y tipos de datos
        try:
            cantidad = int(cantidad_str)
            if cantidad <= 0:
                raise ValueError
        except ValueError:
            messages.error(request, 'La cantidad debe ser un número entero positivo mayor a cero.')
            return redirect('bodega:movimiento')

        # Localizar producto
        item = next((p for p in productos if str(p['id']) == str(producto_id)), None)

        if not item:
            messages.error(request, 'El producto seleccionado no existe en los registros.')
            return redirect('bodega:movimiento')

        # Lógica de bifurcación según tipo de movimiento
        if tipo_movimiento == 'ENTRADA':
            item['stock_actual'] += cantidad
            _guardar_productos(productos)
            messages.success(request, f'Recepción confirmada: Se sumaron {cantidad} unidades a "{item["nombre"]}".')
            return redirect('bodega:panel')

        elif tipo_movimiento == 'SALIDA':
            if item['stock_actual'] < cantidad:
                messages.error(request, f'Quiebre de stock: Stock insuficiente para despachar {cantidad} unidades (Disponibles: {item["stock_actual"]}).')
                return redirect('bodega:movimiento')

            item['stock_actual'] -= cantidad
            _guardar_productos(productos)
            messages.success(request, f'Despacho emitido con éxito hacia {destino}: {cantidad} unidades de "{item["nombre"]}".')
            return redirect('bodega:panel')

    contexto = {
        'modulo': 'Registro de Movimiento Logístico',
        'productos': productos,
        'sucursales': sucursales,
    }
    return render(request, 'bodega/movimiento.html', contexto)


# ==================== AUTENTICACIÓN ====================

def login_view(request):
    if request.user.is_authenticated:
        return redirect('bodega:producto_lista')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            usuario = form.get_user()
            login(request, usuario)
            messages.success(request, f'Bienvenido, {usuario.username}. Sesión iniciada correctamente.')
            siguiente = request.POST.get('next') or request.GET.get('next')
            if siguiente and url_has_allowed_host_and_scheme(
                siguiente, allowed_hosts={request.get_host()}, require_https=request.is_secure()
            ):
                return redirect(siguiente)
            return redirect('bodega:producto_lista')
    else:
        form = AuthenticationForm()

    return render(request, 'bodega/login.html', {
        'form': form,
        'next': request.GET.get('next', ''),
    })


def logout_view(request):
    logout(request)
    messages.info(request, 'Sesión cerrada correctamente. Hasta pronto.')
    return redirect('bodega:login')


# ==================== CRUD PRODUCTOS ====================

@login_required
def producto_lista(request):
    productos = Producto.objects.select_related(
        'categoria', 'marca', 'proveedor_principal', 'ubicacion'
    ).order_by('codigo').all()

    busqueda = request.GET.get('q', '').strip()
    categoria_id = request.GET.get('categoria', '').strip()

    if busqueda:
        productos = productos.filter(
            Q(nombre__icontains=busqueda) | Q(codigo__icontains=busqueda)
        )
    if categoria_id:
        productos = productos.filter(categoria_id=categoria_id)

    paginator = Paginator(productos, 25)
    pagina = paginator.get_page(request.GET.get('page'))

    contexto = {
        'productos': pagina,
        'categorias': Categoria.objects.all().order_by('nombre'),
        'busqueda': busqueda,
        'categoria_filtro': categoria_id,
    }
    return render(request, 'bodega/producto_lista.html', contexto)


@login_required
def producto_crear(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            producto = form.save()
            messages.success(request, f'Producto "{producto.nombre}" creado con éxito.')
            return redirect('bodega:producto_lista')
        messages.error(request, 'Corrija los errores del formulario para guardar el producto.')
    else:
        form = ProductoForm()

    return render(request, 'bodega/producto_form.html', {
        'form': form,
        'titulo': 'Crear Producto',
        'accion': 'Crear',
    })


@login_required
def producto_editar(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            producto = form.save()
            messages.success(request, f'Producto "{producto.nombre}" actualizado con éxito.')
            return redirect('bodega:producto_lista')
        messages.error(request, 'Corrija los errores del formulario para actualizar el producto.')
    else:
        form = ProductoForm(instance=producto)

    return render(request, 'bodega/producto_form.html', {
        'form': form,
        'titulo': 'Editar Producto',
        'accion': 'Guardar Cambios',
        'producto': producto,
    })


@login_required
def producto_eliminar(request, pk):
    producto = get_object_or_404(Producto, pk=pk)

    if request.method == 'POST':
        nombre = producto.nombre
        producto.delete()
        messages.success(request, f'Producto "{nombre}" eliminado permanentemente.')
        return redirect('bodega:producto_lista')

    return render(request, 'bodega/producto_confirmar_eliminar.html', {
        'producto': producto,
    })


# ==================== CRUD DESPACHOS ====================

DetalleDespachoFormSet = inlineformset_factory(
    OrdenDespacho, DetalleDespacho,
    form=DetalleDespachoForm,
    extra=1,
    can_delete=True,
)


@login_required
def despacho_lista(request):
    despachos = OrdenDespacho.objects.select_related('sucursal_destino').annotate(
        total_items=Count('detalles')
    ).order_by('-fecha_creacion')

    paginator = Paginator(despachos, 25)
    pagina = paginator.get_page(request.GET.get('page'))
    return render(request, 'bodega/despacho_lista.html', {'despachos': pagina})


@login_required
def despacho_crear(request):
    if request.method == 'POST':
        form = OrdenDespachoForm(request.POST)
        formset = DetalleDespachoFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            orden = form.save()
            detalles = formset.save(commit=False)
            for detalle in detalles:
                detalle.orden = orden
                detalle.save()
            formset.save_m2m()
            messages.success(request, f'Orden de despacho "{orden.numero_guia}" registrada con sus líneas de detalle.')
            return redirect('bodega:despacho_lista')
        messages.error(request, 'Revise los datos de la guía y las líneas de detalle antes de guardar.')
    else:
        form = OrdenDespachoForm()
        formset = DetalleDespachoFormSet(queryset=DetalleDespacho.objects.none())

    return render(request, 'bodega/despacho_form.html', {
        'form': form,
        'formset': formset,
        'titulo': 'Crear Orden de Despacho',
    })


@login_required
def despacho_detalle(request, pk):
    orden = get_object_or_404(
        OrdenDespacho.objects.select_related('sucursal_destino').prefetch_related(
            'detalles__producto__categoria'
        ),
        pk=pk
    )
    return render(request, 'bodega/despacho_detalle.html', {'orden': orden})

# ==================== GESTIÓN DE USUARIOS ====================

@staff_required
def usuario_lista(request):
    usuarios = User.objects.all().order_by('id')

    busqueda = request.GET.get('q', '').strip()
    if busqueda:
        usuarios = usuarios.filter(
            Q(username__icontains=busqueda)
            | Q(first_name__icontains=busqueda)
            | Q(last_name__icontains=busqueda)
            | Q(email__icontains=busqueda)
        )

    return render(request, 'bodega/usuario_lista.html', {
        'usuarios': usuarios,
        'busqueda': busqueda,
    })


@staff_required
def usuario_crear(request):
    if request.method == 'POST':
        form = UsuarioRegistroForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            messages.success(request, f'Usuario "{usuario.username}" creado con contraseña hasheada de forma segura.')
            return redirect('bodega:usuario_lista')
        messages.error(request, 'Corrija los errores del formulario para crear el usuario.')
    else:
        form = UsuarioRegistroForm()

    return render(request, 'bodega/usuario_form.html', {
        'form': form,
        'titulo': 'Crear Usuario',
        'accion': 'Crear Usuario',
        'url_volver': 'bodega:usuario_lista',
    })


@staff_required
def usuario_editar(request, pk):
    usuario = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = UsuarioEdicionForm(request.POST, instance=usuario)
        if form.is_valid():
            usuario = form.save()
            messages.success(request, f'Usuario "{usuario.username}" actualizado con éxito.')
            return redirect('bodega:usuario_lista')
        messages.error(request, 'Corrija los errores del formulario para actualizar el usuario.')
    else:
        form = UsuarioEdicionForm(instance=usuario)

    return render(request, 'bodega/usuario_form.html', {
        'form': form,
        'titulo': f'Editar Usuario: {usuario.username}',
        'accion': 'Guardar Cambios',
        'url_volver': 'bodega:usuario_lista',
        'usuario': usuario,
    })


@staff_required
def usuario_toggle_activo(request, pk):
    if request.method != 'POST':
        return redirect('bodega:usuario_lista')

    usuario = get_object_or_404(User, pk=pk)

    if usuario == request.user and usuario.is_active:
        messages.error(request, 'No puedes desactivar tu propia cuenta de administrador.')
        return redirect('bodega:usuario_lista')

    usuario.is_active = not usuario.is_active
    usuario.save(update_fields=['is_active'])

    estado = 'activado' if usuario.is_active else 'desactivado'
    messages.success(request, f'Usuario "{usuario.username}" {estado} correctamente.')
    return redirect('bodega:usuario_lista')


@staff_required
def usuario_eliminar(request, pk):
    if request.method != 'POST':
        return redirect('bodega:usuario_lista')

    usuario = get_object_or_404(User, pk=pk)

    if usuario == request.user:
        messages.error(request, 'No puedes eliminar tu propia cuenta.')
        return redirect('bodega:usuario_lista')

    if request.POST.get('confirmar') != 'SI':
        messages.error(request, 'Eliminación no confirmada. Acción cancelada.')
        return redirect('bodega:usuario_lista')

    nombre = usuario.username
    usuario.delete()
    messages.success(request, f'Usuario "{nombre}" eliminado permanentemente del sistema.')
    return redirect('bodega:usuario_lista')
