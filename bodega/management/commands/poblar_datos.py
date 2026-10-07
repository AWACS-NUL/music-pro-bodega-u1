from django.core.management.base import BaseCommand
from faker import Faker
from bodega.models import (
    Categoria, Marca, Proveedor, ZonaBodega, UbicacionFisica,
    Producto, SucursalDestino, OrdenDespacho, DetalleDespacho, AuditoriaStock
)
import random

fake = Faker('es_ES')

class Command(BaseCommand):
    help = 'Poblar la base de datos con datos coherentes para instrumentos musicales y audio profesional'

    def handle(self, *args, **kwargs):
        self.stdout.write('Iniciando poblar_datos...')

        # Categorías (5+)
        categorias_data = [
            {'nombre': 'Guitarras Eléctricas', 'descripcion': 'Guitarras eléctricas y accesorios'},
            {'nombre': 'Bajos', 'descripcion': 'Bajos eléctricos y de contrapunteo'},
            {'nombre': 'Teclados y Pianos', 'descripcion': 'Sintetizadores, pianos digitales y órganos'},
            {'nombre': 'Baterías y Percusión', 'descripcion': 'Baterías acústicas, electrónicas y percusión'},
            {'nombre': 'Audio Profesional', 'descripcion': 'Equipos de sonido, mezcla y grabación'},
            {'nombre': 'Cuerdas Frotadas', 'descripcion': 'Violines, violas, cellos y contrabajos'},
            {'nombre': 'Vientos', 'descripcion': 'Saxofones, trompetas, flautas y clarinetes'},
        ]

        for cat_data in categorias_data:
            Categoria.objects.get_or_create(
                nombre=cat_data['nombre'],
                defaults={'descripcion': cat_data['descripcion']}
            )

        categorias = list(Categoria.objects.all())
        self.stdout.write(f'Categorías creadas: {len(categorias)}')

        # Marcas (5+)
        marcas_data = [
            {'nombre': 'Fender', 'pais_origen': 'Estados Unidos'},
            {'nombre': 'Gibson', 'pais_origen': 'Estados Unidos'},
            {'nombre': 'Yamaha', 'pais_origen': 'Japón'},
            {'nombre': 'Roland', 'pais_origen': 'Japón'},
            {'nombre': 'Pearl', 'pais_origen': 'Japón'},
            {'nombre': 'Shure', 'pais_origen': 'Estados Unidos'},
            {'nombre': 'Ibanez', 'pais_origen': 'Japón'},
        ]

        for marca_data in marcas_data:
            Marca.objects.get_or_create(
                nombre=marca_data['nombre'],
                defaults={'pais_origen': marca_data['pais_origen']}
            )

        marcas = list(Marca.objects.all())
        self.stdout.write(f'Marcas creadas: {len(marcas)}')

        # Proveedores (5+)
        proveedores_data = [
            {'rut': '76.123.456-7', 'razon_social': 'Importadora Musical Andina SpA', 'contacto_email': 'contacto@andina.cl', 'telefono': '+56 2 2345 6789'},
            {'rut': '81.234.567-8', 'razon_social': 'Distribuidora Audio Pro Ltda', 'contacto_email': 'ventas@audiopro.cl', 'telefono': '+56 2 2987 6543'},
            {'rut': '79.345.678-9', 'razon_social': 'Instrumentos del Sur SpA', 'contacto_email': 'pedidos@instrumentsur.cl', 'telefono': '+56 9 8765 4321'},
            {'rut': '77.456.789-0', 'razon_social': 'Rock Import S.A.', 'contacto_email': 'rock@import.cl', 'telefono': '+56 2 2456 7890'},
            {'rut': '83.567.890-1', 'razon_social': 'Clásica Musical Ltda', 'contacto_email': 'info@classicamusical.cl', 'telefono': '+56 2 2678 9012'},
            {'rut': '78.678.901-2', 'razon_social': 'Tech Sound SpA', 'contacto_email': 'tech@sound.cl', 'telefono': '+56 9 7654 3210'},
        ]

        for prov_data in proveedores_data:
            Proveedor.objects.get_or_create(
                rut=prov_data['rut'],
                defaults={
                    'razon_social': prov_data['razon_social'],
                    'contacto_email': prov_data['contacto_email'],
                    'telefono': prov_data['telefono']
                }
            )

        proveedores = list(Proveedor.objects.all())
        self.stdout.write(f'Proveedores creados: {len(proveedores)}')

        # Zonas de Bodega
        zonas_data = [
            {'codigo_zona': 'ZONA-A', 'nombre': 'Zona Alta - Instrumentos de Cuerda', 'temperatura_controlada': True},
            {'codigo_zona': 'ZONA-B', 'nombre': 'Zona Baja - Audio y Electrónica', 'temperatura_controlada': True},
            {'codigo_zona': 'ZONA-C', 'nombre': 'Zona Central - Percusión', 'temperatura_controlada': False},
            {'codigo_zona': 'ZONA-D', 'nombre': 'Zona Destino - Despachos', 'temperatura_controlada': False},
        ]

        for zona_data in zonas_data:
            ZonaBodega.objects.get_or_create(
                codigo_zona=zona_data['codigo_zona'],
                defaults={
                    'nombre': zona_data['nombre'],
                    'temperatura_controlada': zona_data['temperatura_controlada']
                }
            )

        zonas = list(ZonaBodega.objects.all())
        self.stdout.write(f'Zonas creadas: {len(zonas)}')

        # Ubicaciones Físicas (múltiples por zona)
        ubicaciones_count = 0
        for zona in zonas:
            for pasillo in ['A', 'B', 'C']:
                for estante in range(1, 4):
                    for nivel in range(1, 4):
                        UbicacionFisica.objects.get_or_create(
                            zona=zona,
                            pasillo=pasillo,
                            estante=str(estante),
                            nivel=str(nivel)
                        )
                        ubicaciones_count += 1

        ubicaciones = list(UbicacionFisica.objects.all())
        self.stdout.write(f'Ubicaciones físicas creadas: {ubicaciones_count}')

        # Productos (20+)
        productos_data = [
            {'codigo': 'SKU-GTR-001', 'nombre': 'Stratocaster Standard', 'categoria': 'Guitarras Eléctricas', 'marca': 'Fender', 'precio': 450000, 'stock': 15},
            {'codigo': 'SKU-GTR-002', 'nombre': 'Les Paul Classic', 'categoria': 'Guitarras Eléctricas', 'marca': 'Gibson', 'precio': 650000, 'stock': 8},
            {'codigo': 'SKU-GTR-003', 'nombre': 'Telecaster Player', 'categoria': 'Guitarras Eléctricas', 'marca': 'Fender', 'precio': 380000, 'stock': 12},
            {'codigo': 'SKU-GTR-004', 'nombre': 'RG550 Genesis', 'categoria': 'Guitarras Eléctricas', 'marca': 'Ibanez', 'precio': 320000, 'stock': 10},
            {'codigo': 'SKU-BAS-001', 'nombre': 'Jazz Bass Active', 'categoria': 'Bajos', 'marca': 'Fender', 'precio': 420000, 'stock': 9},
            {'codigo': 'SKU-BAS-002', 'nombre': 'BB 435', 'categoria': 'Bajos', 'marca': 'Yamaha', 'precio': 280000, 'stock': 14},
            {'codigo': 'SKU-KEY-001', 'nombre': 'Montage 8', 'categoria': 'Teclados y Pianos', 'marca': 'Yamaha', 'precio': 950000, 'stock': 5},
            {'codigo': 'SKU-KEY-002', 'nombre': 'Juno-DS88', 'categoria': 'Teclados y Pianos', 'marca': 'Roland', 'precio': 520000, 'stock': 7},
            {'codigo': 'SKU-KEY-003', 'nombre': 'P-125', 'categoria': 'Teclados y Pianos', 'marca': 'Yamaha', 'precio': 380000, 'stock': 11},
            {'codigo': 'SKU-DRM-001', 'nombre': 'Export Double', 'categoria': 'Baterías y Percusión', 'marca': 'Pearl', 'precio': 680000, 'stock': 6},
            {'codigo': 'SKU-DRM-002', 'nombre': 'TD-27KV', 'categoria': 'Baterías y Percusión', 'marca': 'Roland', 'precio': 890000, 'stock': 4},
            {'codigo': 'SKU-AUD-001', 'nombre': 'SM58', 'categoria': 'Audio Profesional', 'marca': 'Shure', 'precio': 85000, 'stock': 45},
            {'codigo': 'SKU-AUD-002', 'nombre': 'SM7B', 'categoria': 'Audio Profesional', 'marca': 'Shure', 'precio': 280000, 'stock': 12},
            {'codigo': 'SKU-AUD-003', 'nombre': 'GO:MIXER', 'categoria': 'Audio Profesional', 'marca': 'Roland', 'precio': 65000, 'stock': 30},
            {'codigo': 'SKU-AUD-004', 'nombre': 'Micro Cube GX', 'categoria': 'Audio Profesional', 'marca': 'Roland', 'precio': 95000, 'stock': 18},
            {'codigo': 'SKU-AUD-005', 'nombre': 'V-02HD', 'categoria': 'Audio Profesional', 'marca': 'Roland', 'precio': 320000, 'stock': 8},
            {'codigo': 'SKU-AUD-006', 'nombre': 'BR-800', 'categoria': 'Audio Profesional', 'marca': 'Roland', 'precio': 245000, 'stock': 15},
            {'codigo': 'SKU-STR-001', 'nombre': 'Violín Student 4/4', 'categoria': 'Cuerdas Frotadas', 'marca': 'Yamaha', 'precio': 180000, 'stock': 20},
            {'codigo': 'SKU-STR-002', 'nombre': 'Cello Standard', 'categoria': 'Cuerdas Frotadas', 'marca': 'Yamaha', 'precio': 420000, 'stock': 7},
            {'codigo': 'SKU-WIN-001', 'nombre': 'YAS-280', 'categoria': 'Vientos', 'marca': 'Yamaha', 'precio': 380000, 'stock': 9},
            {'codigo': 'SKU-WIN-002', 'nombre': 'Bach Stradivarius', 'categoria': 'Vientos', 'marca': 'Fender', 'precio': 850000, 'stock': 3},
        ]

        for prod_data in productos_data:
            categoria = next((c for c in categorias if c.nombre == prod_data['categoria']), None)
            marca = next((m for m in marcas if m.nombre == prod_data['marca']), None)
            proveedor = random.choice(proveedores)
            ubicacion = random.choice(ubicaciones)

            if categoria and marca:
                Producto.objects.get_or_create(
                    codigo=prod_data['codigo'],
                    defaults={
                        'nombre': prod_data['nombre'],
                        'categoria': categoria,
                        'marca': marca,
                        'proveedor_principal': proveedor,
                        'ubicacion': ubicacion,
                        'stock_actual': prod_data['stock'],
                        'stock_minimo': random.randint(3, 8),
                        'precio_unitario': prod_data['precio']
                    }
                )

        productos = list(Producto.objects.all())
        self.stdout.write(f'Productos creados: {len(productos)}')

        # Sucursales de Destino
        sucursales_data = [
            {'codigo_sucursal': 'SUC-STA-01', 'nombre': 'Santiago Centro', 'direccion': 'Av. Libertador Bernardo O\'Higgins 1234', 'ciudad': 'Santiago'},
            {'codigo_sucursal': 'SUC-PRO-01', 'nombre': 'Providencia', 'direccion': 'Av. Providencia 2000', 'ciudad': 'Santiago'},
            {'codigo_sucursal': 'SUC-LAS-01', 'nombre': 'Las Condes', 'direccion': 'Av. Apoquindo 4000', 'ciudad': 'Santiago'},
            {'codigo_sucursal': 'SUC-VIN-01', 'nombre': 'Viña del Mar', 'direccion': 'Av. Valparaíso 500', 'ciudad': 'Viña del Mar'},
            {'codigo_sucursal': 'SUC-CON-01', 'nombre': 'Concepción', 'direccion': 'Av. Paicaví 300', 'ciudad': 'Concepción'},
        ]

        for suc_data in sucursales_data:
            SucursalDestino.objects.get_or_create(
                codigo_sucursal=suc_data['codigo_sucursal'],
                defaults={
                    'nombre': suc_data['nombre'],
                    'direccion': suc_data['direccion'],
                    'ciudad': suc_data['ciudad']
                }
            )

        sucursales = list(SucursalDestino.objects.all())
        self.stdout.write(f'Sucursales creadas: {len(sucursales)}')

        # Órdenes de Despacho (con detalles)
        estados = ['PENDIENTE', 'DESPACHADO', 'ENTREGADO', 'CANCELADO']
        for i in range(10):
            numero_guia = f'GUIA-2026-{i+1:04d}'
            sucursal = random.choice(sucursales)
            estado = random.choice(estados)

            orden, created = OrdenDespacho.objects.get_or_create(
                numero_guia=numero_guia,
                defaults={
                    'sucursal_destino': sucursal,
                    'estado': estado
                }
            )

            if created:
                # Agregar 2-5 detalles por orden
                num_detalles = random.randint(2, 5)
                productos_seleccionados = random.sample(productos, min(num_detalles, len(productos)))
                
                for producto in productos_seleccionados:
                    cantidad = random.randint(1, 5)
                    DetalleDespacho.objects.create(
                        orden=orden,
                        producto=producto,
                        cantidad_solicitada=cantidad
                    )

        ordenes = list(OrdenDespacho.objects.all())
        detalles = list(DetalleDespacho.objects.all())
        self.stdout.write(f'Órdenes de despacho creadas: {len(ordenes)}')
        self.stdout.write(f'Detalles de despacho creados: {len(detalles)}')

        # Auditorías de Stock
        tipos_ajuste = ['INVENTARIO_FISICO', 'MERMA', 'DEVOLUCION']
        for producto in random.sample(productos, min(15, len(productos))):
            num_auditorias = random.randint(1, 3)
            for _ in range(num_auditorias):
                tipo = random.choice(tipos_ajuste)
                cantidad = random.choice([-5, -3, -2, -1, 1, 2, 3, 5])
                observacion = fake.sentence() if random.random() > 0.3 else ''
                
                AuditoriaStock.objects.create(
                    producto=producto,
                    tipo_ajuste=tipo,
                    cantidad_afectada=cantidad,
                    observacion=observacion
                )

        auditorias = list(AuditoriaStock.objects.all())
        self.stdout.write(f'Auditorías de stock creadas: {len(auditorias)}')

        self.stdout.write(self.style.SUCCESS('Base de datos poblada exitosamente.'))
