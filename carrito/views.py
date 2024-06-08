
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

global num_elemento 
num_elemento = 30

@login_required
def tienda(request,page=None,search=None):
    profiles = Profile.objects.get(user_id = request.user.id)
    if not (profiles.group_id == 1 or profiles.group_id == 4):
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    # Asegurarse de que el carrito esté inicializado en la sesión
    profiles = Profile.objects.get(user_id = request.user.id)
    if 'carrito' not in request.session:
        request.session['carrito'] = {}
        profiles = Profile.objects.get(user_id = request.user.id)

    if page == None:
        page = request.GET.get('page')
    else:
        page = page
    if request.GET.get('page') == None:
        page = page
    else:
        page = request.GET.get('page')
    #logica que permite recibir la cadena de búsqueda y propoga a través del paginador
    if search == None:
        search = request.GET.get('search')
    else:
        search = search
    if request.GET.get('search') == None:
        search = search
    else:
        search = request.GET.get('search') 
    if request.method == 'POST':
        search = request.POST.get('search') 
        page = None
    #fin logica que permite recibir la cadena de búsqueda y propoga a través del paginador

    producto_all = [] #lista vacia para agrega la salida de la lista ya sea con la cadena de búsqueda o no
    if search == None or search == "None" or search == "" :# si la cadena de búsqueda viene vacia
        producto_array = Producto.objects.filter(producto_state = "Activa").order_by('stock_producto')
        
        for iv in producto_array:
            if iv.stock_producto >0:
                categoria_data = Category.objects.get(producto_id=iv.id)
                categoria_group = categoria_data.category_group
                
                #se guarda la información del producto
                producto_all.append({'id':iv.id,
                                    'nombre_producto':iv.nombre_producto,
                                    'precio_producto':iv.precio_producto,
                                    'stock_producto':iv.stock_producto,
                                    'categoria_data':categoria_group})
                
    else:#si la cadena de búsqueda trae datos
        producto_array =  Producto.objects.filter(Q(nombre_producto__icontains=search)).filter(producto_state = "Activa").order_by('-stock_producto')#Ascendente
        for iv in producto_array:
            if iv.stock_producto >0:
                categoria_data = Category.objects.get(producto_id=iv.id)
                categoria_group = categoria_data.category_group
                #se guarda la información del producto
                producto_all.append({'id':iv.id,
                                    'nombre_producto':iv.nombre_producto,
                                    'precio_producto':iv.precio_producto,
                                    'stock_producto':iv.stock_producto,
                                    'categoria_data':categoria_group})
    paginator = Paginator(producto_all, num_elemento)  
    producto_list = paginator.get_page(page)
    template_name = 'carrito/tienda.html'
    return render(request,template_name,{'profiles':profiles,
                                        'producto_list':producto_list,
                                        'paginator':paginator,
                                        'page':page,
                                        'search':search })





@login_required
def agregar_producto(request, producto_id):
    profiles = Profile.objects.get(user_id=request.user.id)
    carrito = Carrito(request)
    producto = Producto.objects.get(id = producto_id)
    producto_stock = Producto.objects.get(id = producto_id).stock_producto
    cantidad_en_carrito = carrito.get_cantidad(producto_id)

    # Verificar si hay suficiente stock disponible
    if producto_stock > cantidad_en_carrito:
        #Producto.objects.filter(id = producto_id).update(stock_producto = producto_stock -1)
        carrito.agregar(producto)
        return redirect('tienda')
    else:
        messages.add_message(request, messages.INFO, f'No hay stock disponible de {producto.nombre_producto}')
        return redirect('tienda')


@login_required
def eliminar_producto(request, producto_id):
    carrito = Carrito(request)
    producto = Producto.objects.get(id = producto_id)
    carrito.eliminar(producto)
    return redirect('tienda')

@login_required
def restar_producto(request, producto_id):
    carrito = Carrito(request)
    producto = Producto.objects.get(id = producto_id)

    carrito.restar(producto)
    return redirect('tienda')

@login_required
def limpiar_carrito(request):
    carrito = Carrito(request)
    carrito.limpiar()
    return redirect('tienda')

