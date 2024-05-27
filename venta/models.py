from django.db import models
from inventario.models import Producto
# Create your models here.


class Cliente(models.Model):
    
    rut_cliente = models.CharField(max_length = 100,null=True, blank=True, unique= True) 
    nombre_cliente = models.CharField(max_length = 100,null=True, blank=True) 
    apellido_cliente = models.CharField(max_length = 100,null=True, blank=True)  
    correo_cliente = models.CharField(max_length = 100,null=True, blank=True)  
    telefono_cliente = models.IntegerField(null=True, blank=True)
    estado_cliente = models.CharField(max_length=100, null=True, blank=True, default='t')
    creacion_cliente = models.DateTimeField(auto_now_add=True,verbose_name='Fecha Creación')
    actualizacion_cliente = models.DateTimeField(auto_now=True,verbose_name='Fecha Actualización')

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['nombre_cliente']
    
    
        
    def nombre_completo(self):
        return f"{self.nombre_cliente} {self.apellido_cliente}"

    
    def __str__(self):
        return self.nombre_cliente


class Pago(models.Model):
    nombre_pago = models.CharField(max_length = 100,null=True, blank=True) 

    class Meta:
        verbose_name = 'Pago'
        verbose_name_plural = 'Pagos'
        ordering = ['nombre_pago']
    
    def __str__(self):
        return self.nombre_pago


class Venta(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE) 
    pago = models.ForeignKey(Pago, on_delete=models.CASCADE)  
    creacion_venta = models.DateTimeField(auto_now_add=True,verbose_name='Fecha Creación')
    total_venta = models.IntegerField(null=False, blank=False)  
    codigo_venta = models.IntegerField(unique=True, editable=False)  # Editable=False asegura que no sea modificado manualmente
    formatted_codigo_venta = models.CharField(max_length=20, blank=True)  # Campo para almacenar el código formateado con prefijo cv y 0 iniciales

    class Meta:
        verbose_name = 'Venta'
        verbose_name_plural = 'Ventas'
        ordering = ['formatted_codigo_venta']
        
    #*args Este parámetro captura cualquier número de argumentos posicionales adicionales que se pasen a la función. 
    #       Se convierte en una tupla dentro de la función.


    #**kwargs Este parámetro captura cualquier número de argumentos de palabra clave adicionales (es decir, aquellos especificados con nombre)
    # que se pasen a la función. Se convierte en un diccionario dentro de la función.
    
    def save(self, *args, **kwargs):
        if not self.codigo_venta: # si no hay ningun registro 
            last_record = Venta.objects.all().order_by('codigo_venta').last() #busca el ultimo registro, obtiene el codigo de venta
            if last_record:
                self.codigo_venta = last_record.codigo_venta + 1 # lo incrementa en 1
            else:
                self.codigo_venta = 1 # si no hay registro codigo de venta es 1
        
        self.formatted_codigo_venta = f'CV-{str(self.codigo_venta).zfill(5)}' #formatea formatted_codigo_venta con el prefijo CV- 00000codigo_venta
        super().save(*args, **kwargs) # se guarda registro en la base de dato
    
    def __str__(self):
        return self.formatted_codigo_venta
    
    




class VentaProducto(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE) 
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)  
    
    
    class Meta:
        verbose_name = 'VentaProducto'
        verbose_name_plural = 'VentaProductos'
        ordering = ['venta']

            
    def __str__(self):
        #retorna la relacion entre venta y producto
        return f'Venta: {self.venta.formatted_codigo_venta} - Producto: {self.producto.nombre_producto}'

