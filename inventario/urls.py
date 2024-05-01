from django.urls import path
from inventario import views #importará los métodos que generemos en nuestra app
from django.views.decorators.csrf import csrf_exempt

from django.conf import settings
from django.conf.urls.static import static



inventario_urlpatterns = [
   
    path('inventario_main/',views.inventario_main, name='inventario_main'),  
    path('inventario_listado/',views.inventario_listado, name='inventario_listado'),     
    
     

    path('categories_create/',views.categories_create, name='categories_create'),   

    ]
if settings.DEBUG:
    inventario_urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)