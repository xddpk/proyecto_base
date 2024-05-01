from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render,redirect,get_object_or_404
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse
from inventario.models import *
from django.db.models import Avg, Count, Q
from registration.models import Profile
from django.urls import reverse_lazy
# Create your views here.






@login_required
def inventario_main(request):
    profiles = Profile.objects.get(user_id = request.user.id)
    if profiles.group_id != 1 and profiles.group_id != 2:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    template_name = 'inventario/inventario_main.html'
    return render(request,template_name,{'profiles':profiles})



@login_required    
def inventario_listado(request,page=None,search=None):
    
    profiles = Profile.objects.get(user_id = request.user.id)
    if profiles.group_id != 1 and profiles.group_id != 2:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
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
    if search == None or search == "None":# si la cadena de búsqueda viene vacia
        #usuario_count = Producto.objects.filter(is_active='t').count()
        producto_array = Producto.objects.all().order_by('stock_producto')
        
        for iv in producto_array:
            categoria_data = Category.objects.get(producto_id=iv.id)
            #profile = categoria_data.group
            
            #se guarda la información del usuario
            producto_all.append({'id':iv.id,'nombre_producto':iv.nombre_producto,'precio_producto':iv.precio_producto,'stock_producto':iv.stock_producto, 'stock_minimo_producto':iv.stock_minimo_producto,'stock_maximo_producto':iv.stock_maximo_producto,'descripcion_producto':iv.descripcion_producto,'categoria_data':categoria_data})
            print(producto_all)
    else:#si la cadena de búsqueda trae datos
        #h_count = User.objects.filter(is_active='t').filter(nombre__icontains=search).count()
        #Lógica de busqueda por primer nombre, nombre de usuario, los filtra si están activos o no y se ordena por primer nombre de forma ascendente
        producto_array =  Producto.objects.filter(Q(nombre_producto__icontains=search)).order_by('-stock_producto')#Ascendente
        for iv in producto_array:
            categoria_data = Category.objects.get(producto_id=iv.id)
            #profile = categoria_data.group
            #se guarda la información del usuario
            producto_all.append({'id':iv.id,'nombre_producto':iv.nombre_producto,'precio_producto':iv.precio_producto,'stock_producto':iv.stock_producto, 'stock_minimo_producto':iv.stock_minimo_producto,'stock_maximo_producto':iv.stock_maximo_producto,'descripcion_producto':iv.descripcion_producto,'categoria_data':categoria_data})          
    
    #user_array = User.objects.filter(is_active='t').order_by('first_name')
    #categoria_data = Profile.objects.all()
    paginator = Paginator(producto_all, 30)  
    
    producto_list = paginator.get_page(page)
    print(producto_list)
    template_name = 'inventario/inventario_listado.html'
    return render(request,template_name,{'profiles':profiles,'producto_list':producto_list,'paginator':paginator,'page':page })




@login_required
def categories_create(request):

    if request.method=='POST':
        name= request.POST.get('name')
        state=True
        if name=='':
            messages.add_message(request,messages.INFO,'Debe ingresar un nombre para la categoria')
            return('categories_create')    
        categories_save=Category(
            name=name,
            state=state
        )
        categories_save.save()
        messages.add_message(request,messages.INFO,'Categoria creada con exito')
        return redirect('Inventario_main')
    
"""
def categories_edit(request):
    if request.method=='POST':
        name= request.POST.get('name')
        state=True
        Category.objects.filter(pk=request.user.id).update(name=name)
        messages.add_message(request,messages.INFO, 'Nombre de categoria editado con exito')
    categories= Category.objects.get(categories_id=request.categories.id)
    template_name=''
    return  render(request,template_name,{'categories': categories})
def categories_delete(request):
    if request.method == 'POST':
        name= request.POST.get('name')
        Categories.objects.get(name=name).delete()
        messages.add_message(request, messages.INFO, 'Categoria eliminada')
    template_name=''
    categories= Categories.objects.get(categories_id=request.categories.id)
    return  render(request,template_name,{'categories': categories})

"""