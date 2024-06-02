from django.db import models
from inventario.models import *
# Create your models here.
from django import forms

class Proveedor(models.Model):
    
    rut_proveedor = models.CharField(max_length = 100,null=True, blank=True) 
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


class Direccion(models.Model):
    numero_direccion = models.IntegerField(null=True, blank=True, default=0)
    nombre_calle = models.CharField(max_length=100, null=True, blank=True, default='')
    departamento = models.IntegerField(null=True, blank=True, default=0)
    piso = models.IntegerField(null=True, blank=True, default=0)
    comuna = models.ForeignKey(Comuna, on_delete=models.CASCADE) 

    def obtener_direccion(self):
        partes = [
            self.nombre_calle,
            str(self.numero_direccion) if self.numero_direccion else '',
            f"Depto. {self.departamento}" if self.departamento else '',
            f"Piso {self.piso}" if self.piso else ''
        ]
        direccion = ' '.join(partes).strip()
        return direccion
    
    class Meta:
        verbose_name = 'Direccion'
        verbose_name_plural = 'Direcciones'
        ordering = ['numero_direccion']
    
    def __str__(self):
        return str(self.numero_direccion or '')
    
    
    
class ProveedorDireccion(models.Model):
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE) 
    direccion = models.ForeignKey(Direccion, on_delete=models.CASCADE) 
    

    class Meta:
        verbose_name = 'ProveedorDireccion'
        verbose_name_plural = 'ProveedorDirecciones'  
        ordering = ['proveedor']


class OrdenProducto(models.Model):
    nombre_producto = models.CharField(max_length=100, null=True, blank=True)
    cantidad_producto = models.IntegerField(null=True, blank=True)
    precio_producto = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    orden = models.ForeignKey(Orden, on_delete=models.CASCADE) 
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE) 

    def calcular_total(self):
        total = self.precio_producto * self.cantidad_producto
        return total

    def __str__(self):
        return f"{self.nombre_producto} - {self.orden}"  # Aquí puedes personalizar cómo quieres representar el objeto OrdenProducto

    class Meta:
        verbose_name = 'OrdenProducto'
        verbose_name_plural = 'OrdenProductos'  
        ordering = ['cantidad_producto']

    def __str__(self):
        return str(self.numero_direccion or '')
class OrdenProductoForm(forms.ModelForm):
    class Meta:
        model = OrdenProducto
        fields = ['nombre_producto', 'cantidad_producto', 'precio_producto','orden','producto']
    def __str__(self):
        return str(self.numero_direccion or '')