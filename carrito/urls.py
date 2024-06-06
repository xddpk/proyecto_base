from django.urls import path
from inventario import views #importará los métodos que generemos en nuestra app
from django.views.decorators.csrf import csrf_exempt

from django.conf import settings
from django.conf.urls.static import static
from carrito import views



carrito_urlpatterns = [
    path('tienda/',views.tienda, name='tienda'),  
    path('tienda/<groups>/<page>/',views.tienda, name='tienda'),  
    path('agregar/<producto_id>/',views.agregar_producto, name='Add'),     
    path('eliminar/<producto_id>/',views.eliminar_producto, name='Del'),     
    path('restar/<producto_id>/',views.restar_producto, name='Sub'),     
    path('limpiar/',views.limpiar_carrito, name='CLS'),     
    ]


if settings.DEBUG:
    carrito_urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)