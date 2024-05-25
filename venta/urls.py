from django.urls import path
from inventario import views #importará los métodos que generemos en nuestra app
from django.views.decorators.csrf import csrf_exempt

from django.conf import settings
from django.conf.urls.static import static
from venta import views



venta_urlpatterns = [
    path('venta_main/',views.venta_main, name='venta_main'),  
    
    ]


if settings.DEBUG:
    venta_urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)