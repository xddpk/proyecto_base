from django.urls import path
from inventario import views #importará los métodos que generemos en nuestra app
from django.views.decorators.csrf import csrf_exempt

from django.conf import settings
from django.conf.urls.static import static
from proveedor import views



proveedor_urlpatterns = [
    path('proveedor_main/',views.proveedor_main, name='proveedor_main'),  
    path('proveedor_create/',views.proveedor_create, name='proveedor_create'),   
    path('load-comunas/', views.load_comunas, name='load_comunas'),
    path('proveedor_save/',views.proveedor_save, name='proveedor_save'), 
    
    path('proveedor_block/<proveedor_id>/',views.proveedor_block, name='proveedor_block'),
    path('proveedor_activate/<proveedor_id>',views.proveedor_activate, name='proveedor_activate'),
    path('proveedor_delete/<proveedor_id>',views.proveedor_delete, name='proveedor_delete'),
    path('edit_proveedor/<proveedor_id>/',views.edit_proveedor, name='edit_proveedor'),
    
     
    
    path('proveedor_lista_activo/',views.proveedor_lista_activo, name='proveedor_lista_activo'),     
    path('proveedor_lista_activo/<groups>/<page>/',views.proveedor_lista_activo, name='proveedor_lista_activo'),  
    path('proveedor_lista_bloqueado/',views.proveedor_lista_bloqueado, name='proveedor_lista_bloqueado'),     
    path('proveedor_lista_bloqueado/<groups>/<page>/',views.proveedor_lista_bloqueado, name='proveedor_lista_bloqueado'), 
    ]


if settings.DEBUG:
    proveedor_urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)