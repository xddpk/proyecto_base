from django.db import models
from inventario.models import *
# Create your models here.

class Proveedor(models.Model):
    
    nombre_proveedor = models.CharField(max_length = 100,null=True, blank=True)  
    correo_proveedor = models.CharField(max_length = 100,null=True, blank=True)  
    telefono_proveedor = models.IntegerField(null=True, blank=True)
    estado_proveedor = models.CharField(max_length=100, null=True, blank=True, default='t')

    class Meta:
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedores'
        ordering = ['nombre_proveedor']
    
    def __str__(self):
        return self.nombre_proveedor

class Orden(models.Model):
    
    numero_orden = models.IntegerField(null=False, blank=False)  
    direccion_orden = models.CharField(max_length= 100, null=False, blank=False)
    telefono_orden = models.IntegerField(null=True, blank=True)
    estado_orden = models.CharField(max_length=100, null=True, blank=True, default='t')
    descuento = models.FloatField(null=True, blank=True)
    tasa = models.FloatField(null=True, blank=True)
    total_impuesto = models.FloatField(null=True, blank=True)
    total_compra = models.FloatField(null=True, blank=True)
    creacion = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Orden'
        verbose_name_plural = 'Ordenes'
        ordering = ['numero_orden']
    
    def __str__(self):
        return self.numero_orden
    
    
class Region(models.Model):
    nombre_region = models.CharField(max_length=100, null=True, blank=True)
    
    class Meta:
        verbose_name = 'Region'
        verbose_name_plural = 'Regiones'
        ordering = ['nombre_region']
    
    def __str__(self):
        return self.nombre_region

class Comuna(models.Model):
    nombre_comuna = models.CharField(max_length=100, null=True, blank=True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE) 
    
    class Meta:
        verbose_name = 'Comuna'
        verbose_name_plural = 'Comunas'
        ordering = ['nombre_comuna']
    
    def __str__(self):
        return self.nombre_comuna
    
class Calle(models.Model):
    nombre_calle = models.CharField(max_length=100, null=True, blank=True)
    comuna = models.ForeignKey(Comuna, on_delete=models.CASCADE) 
    
    class Meta:
        verbose_name = 'Calle'
        verbose_name_plural = 'Calles'
        ordering = ['nombre_calle']
    
    def __str__(self):
        return self.nombre_calle
    
class Direccion(models.Model):
    numero_dirrecion = models.IntegerField( null=True, blank=True)
    calle = models.ForeignKey(Calle, on_delete=models.CASCADE) 
    
    class Meta:
        verbose_name = 'Direccion'
        verbose_name_plural = 'Direcciones'
        ordering = ['numero_dirrecion']
    
    def __str__(self):
        return self.numero_dirrecion
    
    
    
class ProveedorDireccion(models.Model):
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE) 
    direccion = models.ForeignKey(Direccion, on_delete=models.CASCADE) 
    departamento = models.IntegerField( null=True, blank=True)
    piso = models.IntegerField( null=True, blank=True)

    class Meta:
        verbose_name = 'ProveedorDireccion'
        verbose_name_plural = 'ProveedorDirecciones'  
        ordering = ['proveedor']

class OrdenProducto(models.Model):
    #producto = models.OneToOneField(Producto, on_delete=models.CASCADE, null=True)
    cantidad_producto = models.IntegerField(null=True, blank=True)
    precio_producto = models.IntegerField(null=True, blank=True)
    orden = models.ForeignKey(Orden, on_delete=models.CASCADE) 
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE) 
    
    def calcular_total(self):
        total = self.precio_producto * self.cantidad_producto
        return total

    class Meta:
        verbose_name = 'OrdenProducto'
        verbose_name_plural = 'OrdenProductos'  
        ordering = ['cantidad_producto']
