from django.core.management.base import BaseCommand
from django.db import transaction
from faker import Faker
from bodega.models import (
    Categoria, Marca, Proveedor, ZonaBodega, UbicacionFisica,
    Producto, SucursalDestino, OrdenDespacho, DetalleDespacho, AuditoriaStock
)
import random
import time

fake = Faker('es_ES')

class Command(BaseCommand):
    help = 'Poblar la base de datos con datos coherentes para instrumentos musicales y audio profesional'

    def add_arguments(self, parser):
        parser.add_argument(
            '--cantidad',
            '-c',
            type=int,
            default=100,
            help='Número de productos a generar (por defecto: 100)'
        )

    def handle(self, *args, **kwargs):
        cantidad = kwargs['cantidad']
        tiempo_inicio = time.time()
        
        self.stdout.write(f'Iniciando poblar_datos con {cantidad} productos...')

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

        # Productos (generados dinámicamente según cantidad)
        with transaction.atomic():
            productos_a_crear = []
            productos_existentes = set(Producto.objects.values_list('codigo', flat=True))
            
            for i in range(cantidad):
                codigo = f'SKU-{i+1:06d}'
                if codigo in productos_existentes:
                    continue
                
                categoria = random.choice(categorias)
                marca = random.choice(marcas)
                proveedor = random.choice(proveedores)
                ubicacion = random.choice(ubicaciones)
                
                productos_a_crear.append(
                    Producto(
                        codigo=codigo,
                        nombre=fake.sentence(nb_words=4).rstrip('.').capitalize(),
                        categoria=categoria,
                        marca=marca,
                        proveedor_principal=proveedor,
                        ubicacion=ubicacion,
                        stock_actual=random.randint(0, 100),
                        stock_minimo=random.randint(3, 10),
                        precio_unitario=random.randint(50000, 1000000)
                    )
                )
            
            productos_creados = Producto.objects.bulk_create(productos_a_crear, batch_size=5000)
        
        productos = list(Producto.objects.all())
        self.stdout.write(f'Productos creados: {len(productos_creados)}')

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

        # Órdenes de Despacho (con detalles) - escalado con cantidad
        with transaction.atomic():
            estados = ['PENDIENTE', 'DESPACHADO', 'ENTREGADO', 'CANCELADO']
            cantidad_ordenes = max(10, cantidad // 10)
            
            ordenes_a_crear = []
            detalles_a_crear = []
            guias_existentes = set(OrdenDespacho.objects.values_list('numero_guia', flat=True))
            
            for i in range(cantidad_ordenes):
                numero_guia = f'GUIA-2026-{i+1:06d}'
                if numero_guia in guias_existentes:
                    continue
                
                sucursal = random.choice(sucursales)
                estado = random.choice(estados)
                
                orden = OrdenDespacho(
                    numero_guia=numero_guia,
                    sucursal_destino=sucursal,
                    estado=estado
                )
                ordenes_a_crear.append(orden)
            
            ordenes_creadas = OrdenDespacho.objects.bulk_create(ordenes_a_crear, batch_size=5000)
            
            # Crear detalles para cada orden
            for orden in ordenes_creadas:
                num_detalles = random.randint(2, 5)
                productos_seleccionados = random.sample(productos, min(num_detalles, len(productos)))
                
                for producto in productos_seleccionados:
                    cantidad = random.randint(1, 5)
                    detalles_a_crear.append(
                        DetalleDespacho(
                            orden=orden,
                            producto=producto,
                            cantidad_solicitada=cantidad
                        )
                    )
            
            detalles_creados = DetalleDespacho.objects.bulk_create(detalles_a_crear, batch_size=5000)
        
        ordenes = list(OrdenDespacho.objects.all())
        detalles = list(DetalleDespacho.objects.all())
        self.stdout.write(f'Órdenes de despacho creadas: {len(ordenes_creadas)}')
        self.stdout.write(f'Detalles de despacho creados: {len(detalles_creados)}')

        # Auditorías de Stock - escalado con cantidad
        with transaction.atomic():
            tipos_ajuste = ['INVENTARIO_FISICO', 'MERMA', 'DEVOLUCION']
            cantidad_auditorias = max(15, cantidad // 5)
            
            auditorias_a_crear = []
            productos_muestra = random.sample(productos, min(cantidad_auditorias, len(productos)))
            
            for producto in productos_muestra:
                num_auditorias = random.randint(1, 3)
                for _ in range(num_auditorias):
                    tipo = random.choice(tipos_ajuste)
                    cantidad = random.choice([-5, -3, -2, -1, 1, 2, 3, 5])
                    observacion = fake.sentence() if random.random() > 0.3 else ''
                    
                    auditorias_a_crear.append(
                        AuditoriaStock(
                            producto=producto,
                            tipo_ajuste=tipo,
                            cantidad_afectada=cantidad,
                            observacion=observacion
                        )
                    )
            
            auditorias_creadas = AuditoriaStock.objects.bulk_create(auditorias_a_crear, batch_size=5000)
        
        auditorias = list(AuditoriaStock.objects.all())
        self.stdout.write(f'Auditorías de stock creadas: {len(auditorias_creadas)}')

        # Métricas finales
        tiempo_transcurrido = time.time() - tiempo_inicio
        self.stdout.write(self.style.SUCCESS(f'Base de datos poblada exitosamente.'))
        self.stdout.write(f'Tiempo total: {tiempo_transcurrido:.2f} segundos')
        self.stdout.write(f'Total de registros generados: {len(categorias) + len(marcas) + len(proveedores) + len(zonas) + len(ubicaciones) + len(productos) + len(sucursales) + len(ordenes) + len(detalles) + len(auditorias)}')
