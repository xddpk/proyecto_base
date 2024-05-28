from django.shortcuts import render
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render,redirect,get_object_or_404
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse
from inventario.models import *
from django.db.models import Avg, Count, Q
from registration.models import Profile
from django.urls import reverse_lazy
from extensiones import validacion
# Create your views here.
import xlwt
import pandas as pd
from venta.models import *
from django.http import JsonResponse
#validaciones .py!!!!! <---------------------------------
from extensiones import validacion
from inventario.models import *
from carrito.Carrito import *
# Create your views here.


def tienda(request):
    template_name = 'carrito/tienda.html'
    productos = Producto.objects.all()
    clientes = Cliente.objects.filter(estado_cliente = 't')
    pagos = Pago.objects.all()
    # Asegurarse de que el carrito esté inicializado en la sesión
    if 'carrito' not in request.session:
        request.session['carrito'] = {}
    return render(request, template_name, {'productos': productos, 'clientes':clientes, 'pagos':pagos})


def agregar_producto(request, producto_id):
    carrito = Carrito(request)
    producto = Producto.objects.get(id = producto_id)
    carrito.agregar(producto)
    return redirect('tienda')

def eliminar_producto(request, producto_id):
    carrito = Carrito(request)
    producto = Producto.objects.get(id = producto_id)
    carrito.eliminar(producto)
    return redirect('tienda')

def restar_producto(request, producto_id):
    carrito = Carrito(request)
    producto = Producto.objects.get(id = producto_id)
    carrito.restar(producto)
    return redirect('tienda')

def limpiar_carrito(request):
    carrito = Carrito(request)
    carrito.limpiar()
    return redirect('tienda')


"""
def venta_create(request):
  
    profiles = Profile.objects.get(user_id = request.user.id)
    if profiles.group_id != 1 and profiles.group_id != 4:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    """
    
