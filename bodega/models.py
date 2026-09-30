from django.db import models

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Nombre")
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción")

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"

    def __str__(self):
        return self.nombre

class Marca(models.Model):
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Marca")
    pais_origen = models.CharField(max_length=80, blank=True, null=True, verbose_name="País de Origen")

    class Meta:
        verbose_name = "Marca"
        verbose_name_plural = "Marcas"

    def __str__(self):
        return self.nombre
    
class Proveedor(models.Model):
    rut = models.CharField(max_length=20, unique=True, verbose_name="RUT / ID Tributario")
    razon_social = models.CharField(max_length=150, verbose_name="Razón Social")
    contacto_email = models.EmailField(verbose_name="Correo de Contacto")
    telefono = models.CharField(max_length=30, blank=True, null=True, verbose_name="Teléfono")

    class Meta:
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"

    def __str__(self):
        return self.razon_social
    
class ZonaBodega(models.Model):
    codigo_zona = models.CharField(max_length=10, unique=True, verbose_name="Código de Zona")
    nombre = models.CharField(max_length=80, verbose_name="Nombre de Zona")
    temperatura_controlada = models.BooleanField(default=False, verbose_name="Requiere Climatización")

    class Meta:
        verbose_name = "Zona de Bodega"
        verbose_name_plural = "Zonas de Bodega"

    def __str__(self):
        return f"{self.codigo_zona} - {self.nombre}"
    
class UbicacionFisica(models.Model):
    zona = models.ForeignKey(ZonaBodega, on_delete=models.CASCADE, related_name="ubicaciones")
    pasillo = models.CharField(max_length=10, verbose_name="Pasillo")
    estante = models.CharField(max_length=10, verbose_name="Estante")
    nivel = models.CharField(max_length=10, verbose_name="Nivel")

    class Meta:
        verbose_name = "Ubicación Física"
        verbose_name_plural = "Ubicaciones Físicas"
        unique_together = ('zona', 'pasillo', 'estante', 'nivel')

    def __str__(self):
        return f"{self.zona.codigo_zona} [P:{self.pasillo}-E:{self.estante}-N:{self.nivel}]"