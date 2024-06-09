from django.urls import path
from inventario import views #importará los métodos que generemos en nuestra app
from django.views.decorators.csrf import csrf_exempt

from django.conf import settings
from django.conf.urls.static import static



inventario_urlpatterns = [
    path('inventario_main/',views.inventario_main, name='inventario_main'),  
    path('inventario_listado/',views.inventario_listado, name='inventario_listado'),     
    path('inventario_listado_deactivate/',views.inventario_listado_deactivate, name='inventario_listado_deactivate'), 
 
    path('producto_create/',views.producto_create, name='producto_create'),
    path('producto_save/',views.producto_save, name='producto_save'),     
    path('producto_edit/<producto_id>/',views.producto_edit, name='producto_edit'),
    path('producto_ver/<producto_id>/',views.producto_ver, name='producto_ver'),

    path('producto_delete/<producto_id>',views.producto_delete, name='producto_delete'),
    path('producto_deactivate/<producto_id>/',views.producto_deactivate, name='producto_deactivate'),
    path('producto_activate/<producto_id>/',views.producto_activate, name='producto_activate'),
    path('carga_masiva2/',views.carga_masiva2,name="carga_masiva2"),
    path('carga_masiva_save2/',views.carga_masiva_save2,name="carga_masiva_save2"),
    path('import_inventario/',views.import_inventario,name="import_inventario"),#
    
    path('categories_save/',views.categories_save, name='categories_save'),   



    path('prueba',views.prueba, name='prueba'), 



    path('categories_ver/<categories_id>',views.categories_ver, name='categories_ver'),

    path('inventario_dashboard/',views.inventario_dashboard,name="inventario_dashboard"),
    path('categories_create/',views.categories_create, name='categories_create'),   
    path('categories_save_edit/<categories_id>',views.categories_save_edit, name='categories_save_edit'),


    path('list_categories_active/',views.list_categories, name='list_categories_active'),
    path('list_categories_deactivate/',views.list_categories_deactivate, name='list_categories_deactivate'),  
    path('categories_delete/<categories_id>',views.categories_delete, name='categories_delete'),
    path('categories_edit/<categories_id>/',views.categories_edit, name='categories_edit'),
    path('categories_deactivate/<categories_id>',views.categories_deactivate,name='categories_deactivate'),
    path('categories_activate/<categories_id>',views.categories_activate,name='categories_activate'),




    ]


if settings.DEBUG:
    inventario_urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)