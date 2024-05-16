from django.urls import path
from inventario import views #importará los métodos que generemos en nuestra app
from django.views.decorators.csrf import csrf_exempt

from django.conf import settings
from django.conf.urls.static import static
from proveedor import views



proveedor_urlpatterns = [
    path('proveedor_main/',views.proveedor_main, name='proveedor_main'),  
    
    ]


if settings.DEBUG:
    proveedor_urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)