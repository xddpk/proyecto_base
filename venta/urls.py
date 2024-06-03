from django.urls import path
from inventario import views #importará los métodos que generemos en nuestra app
from django.views.decorators.csrf import csrf_exempt

from django.conf import settings
from django.conf.urls.static import static
from venta import views



venta_urlpatterns = [
    path('venta_main/',views.venta_main, name='venta_main'),  
    
    path('cliente_create/',views.cliente_create, name='cliente_create'),
    path('cliente_save/',views.cliente_save, name='cliente_save'),   
    path('edit_cliente/<cliente_id>/',views.edit_cliente, name='edit_cliente'),   
    path('cliente_lista_principal/',views.cliente_lista_principal, name='cliente_lista_principal'),   
    
    
    path('cliente_lista_activo/',views.cliente_lista_activo, name='cliente_lista_activo'),     
    path('cliente_lista_activo/<groups>/<page>/',views.cliente_lista_activo, name='cliente_lista_activo'),     
    
    
    path('cliente_lista_venta/<cliente_id>/',views.cliente_lista_venta, name='cliente_lista_venta'),     
    path('cliente_lista_venta/<cliente_id>/<groups>/<page>/',views.cliente_lista_venta, name='cliente_lista_venta'), 
    
    path('cliente_lista_venta_detalle/<venta_id>/',views.cliente_lista_venta_detalle, name='cliente_lista_venta_detalle'),     
    path('cliente_lista_venta/<venta_id>/<groups>/<page>/',views.cliente_lista_venta_detalle, name='cliente_lista_venta_detalle'), 
    
    
    path('cliente_lista_bloqueado/',views.cliente_lista_bloqueado, name='cliente_lista_bloqueado'),     
    path('cliente_lista_bloqueado/<groups>/<page>/',views.cliente_lista_bloqueado, name='cliente_lista_bloqueado'), 
    
    path('cliente_block/<cliente_id>/',views.cliente_block, name='cliente_block'),
    path('cliente_activate/<cliente_id>',views.cliente_activate, name='cliente_activate'),
    path('cliente_delete/<cliente_id>',views.cliente_delete, name='cliente_delete'),
    
    path('finalizar_venta/<cliente_id>/',views.finalizar_venta, name='finalizar_venta'), 

    
    
    #path('venta_create/',views.venta_create, name='venta_create'),
    #path('venta_save/',views.venta_save, name='venta_save'),     
    
    ]


if settings.DEBUG:
    venta_urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)