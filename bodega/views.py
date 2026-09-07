import json
from pathlib import Path
from django.shortcuts import render, redirect
from django.contrib import messages

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