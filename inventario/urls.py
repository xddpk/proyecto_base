from django.urls import path
from inventario import views #importará los métodos que generemos en nuestra app
from django.views.decorators.csrf import csrf_exempt

from django.conf import settings
from django.conf.urls.static import static



inventario_urlpatterns = [
    path('inventario_main/',views.inventario_main, name='inventario_main'),  
    path('inventario_listado/',views.inventario_listado, name='inventario_listado'),     
    
    path('producto_create/',views.producto_create, name='producto_create'),   
    path('producto_create3/<producto_id>/',views.producto_create3, name='producto_create3'),
    path('producto_create/',views.producto_create, name='producto_create'),
    path('producto_save/',views.producto_save, name='producto_save'),     
    path('producto_edit/<producto_id>/',views.producto_edit, name='producto_edit'),
    path('producto_delete/<producto_id>',views.producto_delete, name='producto_delete'),
    path('carga_masiva2/',views.carga_masiva2,name="carga_masiva2"),# administrador_carga_masiva
    path('carga_masiva_save2/',views.carga_masiva_save2,name="carga_masiva_save2"),#administrador_carga_masiva_save
    path('import_inventario/',views.import_inventario,name="import_inventario"),#administrador
    path('categories_create/',views.categories_create, name='categories_create'),   
    path('categories_save/',views.categories_save, name='categories_save'),   
    path('inventario_dashboard/',views.inventario_dashboard,name="inventario_dashboard"),
    path('categories_create/',views.categories_create, name='categories_create'),   
    path('categories_save/',views.categories_save, name='categories_save'),
    path('categories_save_edit/<categories_id>',views.categories_save_edit, name='categories_save_edit'),
    path('list_categories/',views.list_categories, name='list_categories'), 
    path('categories_delete/<categories_id>',views.categories_delete, name='categories_delete'),
    path('categories_edit/<categories_id>/',views.categories_edit, name='categories_edit'),
    ]


if settings.DEBUG:
    inventario_urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)