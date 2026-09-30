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