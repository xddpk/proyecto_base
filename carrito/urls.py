from django.urls import path
from inventario import views #importará los métodos que generemos en nuestra app
from django.views.decorators.csrf import csrf_exempt

from django.conf import settings
from django.conf.urls.static import static
from carrito import views



carrito_urlpatterns = [
    path('tienda/',views.tienda, name='tienda'),  
    #path('venta_create/',views.venta_create, name='venta_create'),
    #path('venta_save/',views.venta_save, name='venta_save'),     
    
    ]