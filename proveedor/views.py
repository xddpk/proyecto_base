
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
from django.db.models import F

# Create your views here.
import xlwt
import pandas as pd
from proveedor.models import *
from django.http import JsonResponse
#validaciones .py!!!!! <---------------------------------
from extensiones import validacion
# Create your views here.
#numero de elementos para el listado
global num_elemento 
num_elemento = 30
from django.views import View
from .models import ProductoForm

class AgregarProductosView(View):
    def get(self, request):
        # Aquí puedes pasar los productos y perfiles necesarios al template
        productos = Producto.objects.all()
        profiles = request.user.profile  # Suponiendo que el perfil está relacionado con el usuario
        return render(request, 'template_name.html', {'productos': productos, 'profiles': profiles})

    def post(self, request):
        cantidad = request.POST.getlist('cantidad[]')
        precio = request.POST.getlist('precio[]')

        for cantidad, precio in zip( cantidad, precio):
            OrdenProducto.objects.create( cantidad=cantidad, precio=precio)
        
        return redirect('proveedor/proveedor_main.html')  # Redirige a una página de éxito o donde desees    

def buscar_y_redirigir(request):
    productos = Producto.objects.all()
    return render(request, 'proveedor/proveedor_main3.html', {'productos': productos})


@login_required
def proveedor_main(request):
    profiles = Profile.objects.get(user_id = request.user.id)
    if profiles.group_id != 1 and profiles.group_id != 3:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    template_name = 'proveedor/proveedor_main.html'
    return render(request,template_name,{'profiles':profiles})
@login_required
def proveedor_main4(request):
    profiles = Profile.objects.get(user_id = request.user.id)
    if profiles.group_id != 1 and profiles.group_id != 3:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    template_name = 'proveedor/proveedor_main4.html'
    return render(request,template_name,{'profiles':profiles})
@login_required
def proveedor_main2(request):
    profiles = Profile.objects.get(user_id = request.user.id)
    if profiles.group_id != 1 and profiles.group_id != 3:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    template_name = 'proveedor/proveedor_main2.html'
    return render(request,template_name,{'profiles':profiles})


@login_required
def proveedor_main3(request, producto_id=None):
    profiles = Profile.objects.get(user_id=request.user.id)
    
    if profiles.group_id not in [1, 3]:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    
    productos = Producto.objects.all()
    template_name = 'proveedor/proveedor_main3.html'
    proveedores = Proveedor.objects.all()
    
    return render(request, template_name, {'profiles': profiles, 'productos': productos,'proveedores': proveedores})


@login_required
def agregar_productos(request):
    if request.method == 'POST':
        # Creamos una lista vacía para almacenar los productos creados
        productos_creados = []
        proveedor = request.POST['proveedor']
        email = request.POST['email']
        fecha = request.POST['fecha']
        numero = request.POST['numero']

        # Crear la orden
        orden = Orden(proveedor_id=proveedor, telefono_orden=email, creacion=fecha, nota_orden=numero)
        orden.save()
        # Iteramos sobre los datos del formulario
        for i in range(len(request.POST.getlist('nombre[]'))):
            nombre = request.POST.getlist('nombre[]')[i]
            cantidad = request.POST.getlist('cantidad[]')[i]
            precio = request.POST.getlist('precio[]')[i]
            productos = Producto.objects.filter(nombre_producto=nombre)
            producto = productos.first() 
            "Producto.objects.filter(id=producto.id).update(stock_producto=F('stock_producto') + cantidad)"


            # Creamos una instancia de ProductoForm con los datos del formulario
            """form = OrdenProductoForm({'nombre_producto': nombre, 'cantidad_producto': cantidad, 'precio_producto': precio, 'orden_id': orden, 'producto_id': producto})

            # Verificamos si el formulario es válido
            if form.is_valid():
                # Guardamos el producto en la base de datos
                producto = form.save()
                # Añaidimos el producto creado a la lista de productos creados
                productos_creados.append(producto)
            else:
                # Si el formulario no es válido, podrías manejarlo de alguna manera, como mostrar un mensaje de error
                pass"""
            OrdenProducto.objects.create(
                    nombre_producto=nombre,
                    cantidad_producto=cantidad,
                    precio_producto=precio,
                    orden=orden,
                    producto=producto,
                    

                )
                # Redireccionamos a alguna página después de agregar los productos
        return redirect('proveedor_main')

    else:
        # Si la solicitud no es de tipo POST, renderizamos el formulario vacío
        form = ProductoForm()
        return render(request, 'proveedor_main.html', {'form': form})
    
@login_required
def proveedor_create(request):
    profiles = Profile.objects.get(user_id = request.user.id)
    if profiles.group_id != 1 and profiles.group_id != 3:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    template_name = 'proveedor/proveedor_create.html'
    regiones = Region.objects.all()
    return render(request,template_name,{'regiones':regiones, 'profiles':profiles})

@login_required
def direccion_create(request, proveedor_id):
    profiles = Profile.objects.get(user_id = request.user.id)
    if profiles.group_id != 1 and profiles.group_id != 3:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    template_name = 'proveedor/direccion_create.html'
    regiones = Region.objects.all()
    return render(request,template_name,{'regiones':regiones, 'profiles':profiles, 'id':proveedor_id})



@login_required
def direccion_save(request, proveedor_id):
    profiles = Profile.objects.get(user_id = request.user.id)
    if profiles.group_id != 1 and profiles.group_id != 3:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')

    if request.method=='POST':
        
        region= request.POST.get('region')
        comuna= request.POST.get('comuna')
        calle= request.POST.get('calle')
        numero= request.POST.get('numero')
        departamento= request.POST.get('departamento')
        piso= request.POST.get('piso')
        state=True
        validar = True


        if validacion.validar_calle(calle)==False:
                messages.add_message(request, messages.INFO, 'Ingresado incorrectamente')
                validar=False
        if validacion.validar_int(numero)==False:
                messages.add_message(request, messages.INFO, 'Ingresado incorrectamente')
                validar=False
        if validacion.validar_depto(departamento)==False:
                messages.add_message(request, messages.INFO, 'Ingresado incorrectamente')
                validar=False
        if validacion.validar_int(piso)==False:
                messages.add_message(request, messages.INFO, 'Ingresado incorrectamente')
                validar=False
        if validar==True:

            direccion_save = Direccion (
                nombre_calle = calle, 
                numero_direccion = numero,
                departamento = departamento,
                piso = piso,
                comuna_id = comuna,
                )
            direccion_save.save()
            
            proveedordireccion_save = ProveedorDireccion (

                direccion_id = direccion_save.id,
                proveedor_id = proveedor_id,
                
            )
            
            proveedordireccion_save.save()

            
            
            messages.add_message(request,messages.INFO,'Dirección creado con exito')
    return redirect('proveedor_main')

# views.py


def load_comunas(request):
    region_id = request.GET.get('region_id')
    comunas = Comuna.objects.filter(region_id=region_id).all()
    return JsonResponse(list(comunas.values('id', 'nombre_comuna')), safe=False)


@login_required
def proveedor_save(request):

    if request.method=='POST':
        rut  = request.POST.get('rut')
        name= request.POST.get('name')
        region= request.POST.get('region')
        comuna= request.POST.get('comuna')
        calle= request.POST.get('calle')
        numero= request.POST.get('numero')
        mobile= request.POST.get('mobile')
        correo= request.POST.get('email')
        departamento= request.POST.get('departamento')
        piso= request.POST.get('piso')
        state=True
        validar = True
        rut_exist = Proveedor.objects.filter(rut_proveedor=rut).count()
        mail_exist = Proveedor.objects.filter(correo_proveedor=correo).count()
        
        if rut_exist==1:
                messages.add_message(request, messages.INFO, 'Rut ya esta registrado')
                validar=False
        if mail_exist==1:
                messages.add_message(request, messages.INFO, 'Correo ya esta registrado')
                validar=False
        if validacion.validar_rut(rut)==False:
                messages.add_message(request, messages.INFO, 'rut Ingresado incorrectamente')
                validar=False
        if validacion.validar_soloString(name)==False:
                messages.add_message(request, messages.INFO, 'nombre Ingresado incorrectamente')
                validar=False
        if validacion.validar_calle(calle)==False:
                messages.add_message(request, messages.INFO, 'calle Ingresado incorrectamente')
                validar=False
        if validacion.validar_int(numero)==False:
                messages.add_message(request, messages.INFO, 'numero Ingresado incorrectamente')
                validar=False
        if validacion.validar_numCelular(mobile)==False:
                messages.add_message(request, messages.INFO, 'mobile Ingresado incorrectamente')
                validar=False
        if validacion.validar_email(correo)==False:
                messages.add_message(request, messages.INFO, 'correo Ingresado incorrectamente')
                validar=False
        if validacion.validar_depto(departamento)==False:
                messages.add_message(request, messages.INFO, 'depa Ingresado incorrectamente')
                validar=False
        if validacion.validar_piso(piso)==False:
                messages.add_message(request, messages.INFO, 'pisoIngresado incorrectamente')
                validar=False
        if validar==True:
            proveedor_save=Proveedor(
                rut_proveedor = rut,
                nombre_proveedor=name,
                correo_proveedor=correo,
                telefono_proveedor=mobile,
                estado_proveedor="t",
            )
            proveedor_save.save()

            direccion_save = Direccion (
                nombre_calle = calle, 
                numero_dirrecion = numero,
                departamento = departamento,
                piso = piso,
                comuna_id = comuna,
                
                
                )
            direccion_save.save()
            
            proveedordireccion_save = ProveedorDireccion (

                direccion_id = direccion_save.id,
                proveedor_id = proveedor_save.id,
                
            )
            
            proveedordireccion_save.save()

            
            
            messages.add_message(request,messages.INFO,'Proveedor creado con exito')
    return redirect('proveedor_main')


def proveedor_lista_main(request):
    profiles = Profile.objects.get(user_id = request.user.id)
    
    if profiles.group_id != 1 and profiles.group_id != 3:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    
    template_name = 'proveedor/proveedor_lista_main.html'
    return render(request,template_name,{'profiles':profiles})

@login_required
def editar_orden(request, orden_id):
    profiles = Profile.objects.get(user_id=request.user.id)
    validar = True
    
    if profiles.group_id != 1 and profiles.group_id != 3:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a un área para la que no tiene permisos')
        return redirect('check_group_main')

    if request.method == 'POST':
        form = OrdenForm(request.POST)
        orden=Orden
        if form.is_valid():
            orden = form.save(commit=False)
            orden_id = request.POST.get('orden_id')
            numero_orden = request.POST.get('numero_orden')
            direccion_orden = request.POST.get('direccion_orden')
            telefono_orden = request.POST.get('telefono_orden')
            estado_orden = request.POST.get('estado_orden')
            descuento = request.POST.get('descuento')
            tasa = request.POST.get('tasa')
            total_impuesto = request.POST.get('total_impuesto')
            total_compra = request.POST.get('total_compra')
            nota_orden = request.POST.get('nota_orden')

            orden.orden_id = orden_id
            Orden.objects.filter(pk = orden_id).update(numero_orden=numero_orden) 
            Orden.objects.filter(pk = orden_id).update(direccion_orden=direccion_orden)
            Orden.objects.filter(pk = orden_id).update(telefono_orden=telefono_orden)
            Orden.objects.filter(pk = orden_id).update(numero_orden=numero_orden)
            Orden.objects.filter(pk = orden_id).update(nota_orden=nota_orden)
            
            messages.success(request, 'Orden de compra editada exitosamente.')
            return redirect('orden_compra_activo')
        else:
            messages.error(request, 'Hubo un error al editar la orden de compra. Por favor, revise los datos ingresados.')
    else:
        orden = Orden.objects.get(pk=orden_id)
        form = OrdenForm(instance=orden)
    
    return render(request, 'proveedor/editar_orden.html', {'profiles': profiles, 'form': form, 'orden_id': orden_id , 'orden': orden})

@login_required
def edit_proveedor(request,proveedor_id,page=None,search=None):
    profiles = Profile.objects.get(user_id = request.user.id)
    validar = True
    if profiles.group_id != 1 and profiles.group_id != 3 :
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
        rut  = request.POST.get('rut')
        name= request.POST.get('name')
        mobile= request.POST.get('mobile')
        correo= request.POST.get('email')
        rut_exist = Proveedor.objects.filter(rut_proveedor=rut).count()
        mail_exist = Proveedor.objects.filter(correo_proveedor=correo).count()
        proveedor_data_count = Proveedor.objects.filter(pk=proveedor_id).count()
        proveedor_data = Proveedor.objects.get(pk=proveedor_id)
        if proveedor_data_count == 1:
            if validacion.validar_soloString(name)==False:
                messages.add_message(request, messages.INFO, 'Ingresado incorrectamente')
                validar=False
            if validacion.validar_rut(rut)==False:
                messages.add_message(request, messages.INFO, 'Ingresado incorrectamente')
                validar=False
            if validacion.validar_numCelular(mobile)==False:
                messages.add_message(request, messages.INFO, 'Ingresado incorrectamente')
                validar=False
            if validacion.validar_email(correo)==False:
                messages.add_message(request, messages.INFO, 'Ingresado incorrectamente')
                validar=False
                
            if validar == True:
                Proveedor.objects.filter(pk = proveedor_id).update(nombre_proveedor = name.capitalize())
                Proveedor.objects.filter(pk = proveedor_id).update(correo_proveedor = correo)  
                Proveedor.objects.filter(pk = proveedor_id).update(telefono_proveedor = mobile)    
                Proveedor.objects.filter(pk = proveedor_id).update(rut_proveedor = rut)         
                messages.add_message(request, messages.INFO, 'Proveedor '+proveedor_data.nombre_proveedor+' editado con éxito')                             
                return redirect('proveedor_lista_activo')
            #Si no se cumple alguna de las especificaciones lleva aca -Enzo
            
            else:
                messages.add_message(request, messages.INFO, 'Complete segun lo pedido') 
                #que es page                            
                pass
        else:
            messages.add_message(request, messages.INFO, 'Hubo un error al editar el Proveedor '+proveedor_data.nombre_proveedor)
            pass   
    proveedor_data = Proveedor.objects.get(pk=proveedor_id)
    direcciones_all = [] #lista vacia para agrega la salida de la lista ya sea con la cadena de búsqueda o no
    if search == None or search.lower() == "none" or search == '':# si la cadena de búsqueda viene vacia
        proveedordireccion_array = ProveedorDireccion.objects.filter(proveedor_id = proveedor_id)
        for dr in proveedordireccion_array:
            direccion = Direccion.objects.get(pk = dr.direccion_id)
            comuna = Comuna.objects.get(pk = direccion.comuna_id)
            region = Region.objects.get(pk = comuna.region_id)
            direccionc = direccion.obtener_direccion()
            direcciones_all.append({'id':direccion.id,
                                    'proveedor_id': proveedor_id,
                                'comuna':comuna.nombre_comuna,
                                'region': region.nombre_region,
                                'direccion':direccionc}
                                ) 
    
        paginator = Paginator(direcciones_all, num_elemento)  
        direccion_list = paginator.get_page(page)
        template_name = 'proveedor/edit_proveedor.html'
        return render(request,template_name,{'profiles':profiles,'direccion_list':direccion_list,'paginator':paginator,'page':page,'search':search, 'proveedor_data':proveedor_data })

    else:#si la cadena de búsqueda trae datos

        #se filtran todas las tablas ProveedorDireccion que contengan que su registro proveedor_id sea igual al proveedor_que se esta editando
        proveedordireccion_array = ProveedorDireccion.objects.filter(proveedor_id = proveedor_id)


        for dr in proveedordireccion_array:
            print(dr)
            #se consigue la tabla la cual su pk sea igual a la llave foranea de ProveedorDireccion
            direcciones = Direccion.objects.filter(
                
                Q(nombre_calle__icontains=search)|
                Q(numero_direccion__icontains=search)
                    ).filter(pk = dr.direccion_id).order_by('nombre_calle')
            print(direcciones)
            for direccion in direcciones:
            # Iteramos sobre las direcciones encontradas
                comuna = Comuna.objects.get(pk=direccion.comuna_id)
                region = Region.objects.get(pk=comuna.region_id)
                # Obtenemos la representación de la dirección
                direccionc = direccion.obtener_direccion()
                # Agregamos la información a la lista de direcciones
                direcciones_all.append({
                    'id': direccion.id,
                    'comuna': comuna.nombre_comuna,
                    'region': region.nombre_region,
                    'direccion': direccionc
                })
            

            
        
    paginator = Paginator(direcciones_all, num_elemento)  
    direccion_list = paginator.get_page(page)
    template_name = 'proveedor/edit_proveedor.html'
    return render(request,template_name,{'profiles':profiles,'direccion_list':direccion_list,'paginator':paginator,'page':page,'search':search, 'proveedor_data':proveedor_data })
            
@login_required
def ver_proveedor(request, proveedor_id):
    profiles = Profile.objects.get(user_id=request.user.id)
    if profiles.group_id != 1 and profiles.group_id != 2:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main') 
    template_name = 'proveedor/ver_proveedor.html'
    proveedor_data = Proveedor.objects.get(pk=proveedor_id)
    return render(request,template_name,{'proveedor_data':proveedor_data})
@login_required
def ver_orden(request, orden_id):
    profiles = Profile.objects.get(user_id=request.user.id)
    
    if profiles.group_id != 1 and profiles.group_id != 2:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una área para la que no tiene permisos')
        return redirect('check_group_main')
    
    orden = Orden.objects.get(pk=orden_id)
    template_name = 'proveedor/ver_orden.html'
    
    return render(request, template_name, {'orden': orden})

@login_required
def orden_block(request, orden_id):
    profiles = Profile.objects.get(user_id=request.user.id)
    if profiles.group_id not in [1, 3]:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a un área para la que no tiene permisos')
        return redirect('check_group_main')

    try:
        order_data = Orden.objects.get(pk=orden_id)
    except Orden.DoesNotExist:
        messages.add_message(request, messages.INFO, 'La orden no existe')
        return redirect('orden_compra_activo')

    # Actualizar el estado de la orden a 't' (supongo que 't' significa "llegada")
    Orden.objects.filter(pk=orden_id).update(estado_orden='t')

    # Mensaje de éxito
    messages.add_message(request, messages.INFO, 'Orden ha llegado con éxito')

    # Actualizar el stock de los productos asociados a la orden
    ordent = OrdenProducto.objects.filter(orden_id=orden_id)
    for ordert in ordent:
        producto = Producto.objects.get(pk=ordert.producto_id)
        Producto.objects.filter(id=producto.id).update(stock_producto=F('stock_producto') + ordert.cantidad_producto)

    return redirect('orden_compra_activo')
   
   
"""   
@login_required
def orden_delete(request,orden_id):
    profiles = Profile.objects.get(user_id = request.user.id)
    if profiles.group_id != 1 and profiles.group_id != 3:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')

    orden_data_count = Orden.objects.filter(pk=orden_id).count()
    orden_data = OrdenProducto.objects.get(pk=orden_id)
    
    if orden_data_count == 1:
        try:
            #Profile.objects.filter(orden_id=orden_id).delete()
            Proveedor.objects.filter(pk=orden_id).delete()
            ProveedorDireccion.objects.filter(orden_id=orden_id).delete
            messages.add_message(request, messages.INFO, 'Orden  eliminado con éxito')
        except:
            return redirect('proveedor_lista_bloqueado')       
    else:
        messages.add_message(request, messages.INFO, 'Hubo un error al eliminar la Orden ')
        return redirect('proveedor_lista_bloqueado')  """    
        
@login_required
def orden_delete(request,orden_id):
    profiles = Profile.objects.get(user_id=request.user.id)
    if profiles.group_id != 1 and profiles.group_id != 3:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una área para la que no tiene permisos')
        return redirect('check_group_main')

    order_data_count = Orden.objects.filter(pk=orden_id).count()
    order_data = Orden.objects.get(pk=orden_id)     
    if order_data_count == 1:
        Orden.objects.filter(pk=orden_id).update(estado_orden='z')
        messages.add_message(request, messages.INFO, ' Orden ha llegado con éxito')
        return redirect('orden_compra_activo')        
    else:
        messages.add_message(request, messages.INFO, 'Hubo un error con la orden ' )
        return redirect('orden_compra_activo')    
      
@login_required
def orden_activate(request, orden_id):
    profiles = Profile.objects.get(user_id = request.user.id)
    if profiles.group_id != 1 and profiles.group_id != 3:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    order_data_count = Orden.objects.filter(pk=orden_id).count()
    order_data = Orden.objects.get(pk=orden_id)     
    if order_data_count == 1:
        Orden.objects.filter(pk=orden_id).update(estado_orden='t')
        messages.add_message(request, messages.INFO, 'Orden '+order_data.formatted_numero_orden +' activado con éxito')
        return redirect('proveedor_lista_bloqueado')        
    else:
        messages.add_message(request, messages.INFO, 'Hubo un error al activar el Proveedor '+order_data.formatted_numero_orden +'activado')
        return redirect('proveedor_lista_bloqueado')        



@login_required    
def proveedor_lista_activo(request,page=None,search=None):
    profiles = Profile.objects.get(user_id = request.user.id)
    if profiles.group_id != 1 and profiles.group_id != 3:
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
    proveedor_all = [] #lista vacia para agrega la salida de la lista ya sea con la cadena de búsqueda o no
    if search == None or search.lower() == "none":# si la cadena de búsqueda viene vacia
        #usuario_count = proveedor.objects.filter(is_active='t').count()
        proveedor_array = Proveedor.objects.filter(estado_proveedor='t').order_by('nombre_proveedor')
        
        for pr in proveedor_array:
            #se guarda la información del usuario
            proveedor_all.append({'id':pr.id,
                                'nombre_proveedor':pr.nombre_proveedor,
                                'correo_proveedor':pr.correo_proveedor,
                                'telefono_proveedor':pr.telefono_proveedor,
                                'rut_proveedor':pr.rut_proveedor}
                                )
        paginator = Paginator(proveedor_all, num_elemento)  
        proveedor_list = paginator.get_page(page)
        template_name = 'proveedor/proveedor_lista_activo.html'
        return render(request,template_name,{'profiles':profiles,'proveedor_list':proveedor_list,'paginator':paginator,'page':page,'search':search })
            
    else:#si la cadena de búsqueda trae datos
        #h_count = User.objects.filter(is_active='t').filter(nombre__icontains=search).count()
        #Lógica de busqueda por primer nombre, nombre de usuario, los filtra si están activos o no y se ordena por primer nombre de forma ascendente
        proveedor_array =  Proveedor.objects.filter(Q(nombre_proveedor__icontains=search)|Q(rut_proveedor__icontains=search)).filter(estado_proveedor='t').order_by('nombre_proveedor')#Ascendente
        
        for pr in proveedor_array:
            
            #se guarda la información del usuario
            proveedor_all.append({'id':pr.id,
                                'nombre_proveedor':pr.nombre_proveedor,
                                'correo_proveedor':pr.correo_proveedor,
                                'telefono_proveedor':pr.telefono_proveedor,
                                'rut_proveedor':pr.rut_proveedor}
                                )
            
    #user_array = User.objects.filter(is_active='t').order_by('nombre_proveedor')
    #profile_data = Profile.objects.all()
    paginator = Paginator(proveedor_all, num_elemento)  
    proveedor_list = paginator.get_page(page)
    template_name = 'proveedor/proveedor_lista_activo.html'
    return render(request,template_name,{'profiles':profiles,'proveedor_list':proveedor_list,'paginator':paginator,'page':page ,'search':search })
    

@login_required    
def orden_compra_activo(request, page=None, search=None):
    profiles = Profile.objects.get(user_id=request.user.id)
    
    if profiles.group_id not in [1, 3]:  # Verificar permisos
        messages.add_message(request, messages.INFO, 'Intenta ingresar a un área para la que no tienes permisos')
        return redirect('check_group_main')
    
    if page is None:
        page = request.GET.get('page')
    else:
        page = page
        
    if request.GET.get('page') is None:
        page = page
    else:
        page = request.GET.get('page')
        
    # Lógica para recibir la cadena de búsqueda y propagarla a través del paginador
    if search is None:
        search = request.GET.get('search')
    else:
        search = search
        
    if request.GET.get('search') is None:
        search = search
    else:
        search = request.GET.get('search')
        
    if request.method == 'POST':
        search = request.POST.get('search') 
        page = None
    
    # Lógica para construir la lista de órdenes de compra activas
    orden_all = [] 
    
    if search is None or search.lower() == "none": # Si la cadena de búsqueda está vacía
        orden_array = Orden.objects.filter(estado_orden='t').order_by('numero_orden')
        
        for orden in orden_array:
            orden_all.append({
                'numero_orden': orden.formatted_numero_orden,
                'nota_orden': orden.nota_orden,
                'telefono_orden': orden.telefono_orden,
                'estado_orden': orden.estado_orden,
                'proveedor': orden.proveedor,
                'id': orden.id  # Aquí añadimos el id de la orden al contexto
            })
        
        paginator = Paginator(orden_all, 20)  
        orden_list = paginator.get_page(page)
        template_name = 'proveedor/orden_compra_activo.html'
        
        return render(request, template_name, {
            'profiles': profiles,
            'orden_list': orden_list,
            'paginator': paginator,
            'page': page,
            'search': search
        })
            
    else: # Si la cadena de búsqueda trae datos
        orden_array = Orden.objects.filter(numero_orden__icontains=search).filter(estado_orden='t').order_by('numero_orden')
        
        for orden in orden_array:
            orden_all.append({
                'numero_orden': orden.numero_orden,
                'direccion_orden': orden.direccion_orden,
                'telefono_orden': orden.telefono_orden,
                'estado_orden': orden.estado_orden,
                'proveedor': orden.proveedor,
                'id': orden.id  # Aquí añadimos el id de la orden al contexto
            })
            
    paginator = Paginator(orden_all, num_elemento)  
    orden_list = paginator.get_page(page)
    template_name = 'proveedor/orden_compra_activo.html'
    
    return render(request, template_name, {
        'profiles': profiles,
        'orden_list': orden_list,
        'paginator': paginator,
        'page': page,
        'search': search
    })
@login_required    
def orden_compra_finalizada(request, page=None, search=None):
    profiles = Profile.objects.get(user_id=request.user.id)
    
    if profiles.group_id not in [1, 3]:  # Verificar permisos
        messages.add_message(request, messages.INFO, 'Intenta ingresar a un área para la que no tienes permisos')
        return redirect('check_group_main')
    
    if page is None:
        page = request.GET.get('page')
    else:
        page = page
        
    if request.GET.get('page') is None:
        page = page
    else:
        page = request.GET.get('page')
        
    # Lógica para recibir la cadena de búsqueda y propagarla a través del paginador
    if search is None:
        search = request.GET.get('search')
    else:
        search = search
        
    if request.GET.get('search') is None:
        search = search
    else:
        search = request.GET.get('search')
        
    if request.method == 'POST':
        search = request.POST.get('search') 
        page = None
    
    # Lógica para construir la lista de órdenes de compra activas
    orden_all = [] 
    
    if search is None or search.lower() == "none": # Si la cadena de búsqueda está vacía
        orden_array = Orden.objects.filter(estado_orden='z').order_by('numero_orden')
        
        for orden in orden_array:
            orden_all.append({
                'numero_orden': orden.formatted_numero_orden,
                'direccion_orden': orden.direccion_orden,
                'telefono_orden': orden.telefono_orden,
                'estado_orden': orden.estado_orden,
                'proveedor': orden.proveedor,
                'id': orden.id  # Aquí añadimos el id de la orden al contexto
            })
        
        paginator = Paginator(orden_all, 20)  
        orden_list = paginator.get_page(page)
        template_name = 'proveedor/orden_compra_activo.html'
        
        return render(request, template_name, {
            'profiles': profiles,
            'orden_list': orden_list,
            'paginator': paginator,
            'page': page,
            'search': search
        })
            
    else: # Si la cadena de búsqueda trae datos
        orden_array = Orden.objects.filter(numero_orden__icontains=search).filter(estado_orden='z').order_by('numero_orden')
        
        for orden in orden_array:
            orden_all.append({
                'numero_orden': orden.numero_orden,
                'direccion_orden': orden.direccion_orden,
                'telefono_orden': orden.telefono_orden,
                'estado_orden': orden.estado_orden,
                'proveedor': orden.proveedor,
                'id': orden.id  # Aquí añadimos el id de la orden al contexto
            })
            
    paginator = Paginator(orden_all, num_elemento)  
    orden_list = paginator.get_page(page)
    template_name = 'proveedor/orden_compra_activo.html'
    
    return render(request, template_name, {
        'profiles': profiles,
        'orden_list': orden_list,
        'paginator': paginator,
        'page': page,
        'search': search
    })
    
@login_required    
def orden_lista_bloqueada(request, page=None, search=None):
    profiles = Profile.objects.get(user_id=request.user.id)
    if profiles.group_id not in [1, 3]:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    
    if page is None:
        page = request.GET.get('page')
    else:
        page = page
    if request.GET.get('page') is None:
        page = page
    else:
        page = request.GET.get('page')
    
    if search is None:
        search = request.GET.get('search')
    else:
        search = search
    if request.GET.get('search') is None:
        search = search
    else:
        search = request.GET.get('search') 
    
    if request.method == 'POST':
        search = request.POST.get('search')
        page = None
    
    print("search> ", search)
    orden_all = []  # lista vacía para agregar la salida de la lista ya sea con la cadena de búsqueda o no
    
    if search is None or search == "None":  # si la cadena de búsqueda viene vacía
        orden_array = Orden.objects.filter(estado_orden='f').order_by('numero_orden')
        
        for orden in orden_array:
            orden_all.append({
                'id': orden.id,
                'numero_orden': orden.formatted_numero_orden,
                'direccion_orden': orden.direccion_orden,
                'telefono_orden': orden.telefono_orden,
                'estado_orden': orden.estado_orden,
                'proveedor': orden.proveedor.nombre_proveedor if orden.proveedor else ''
            })
        
        paginator = Paginator(orden_all, 20)  
        orden_list = paginator.get_page(page)
        template_name = 'proveedor/orden_lista_bloqueada.html'
        return render(request, template_name, {'profiles': profiles, 'orden_list': orden_list, 'paginator': paginator, 'page': page, 'search': search })
    
    else:  # si la cadena de búsqueda trae datos
        orden_array = Orden.objects.filter(
            Q(formatted_numero_orden__icontains=search) | 
            Q(direccion_orden__icontains=search)
        ).filter(estado_orden='f').order_by('numero_orden')  # Ascendente
        
        for orden in orden_array:
            orden_all.append({
                'id': orden.id,
                'numero_orden': orden.formatted_numero_orden,
                'direccion_orden': orden.direccion_orden,
                'telefono_orden': orden.telefono_orden,
                'estado_orden': orden.estado_orden,
                'proveedor': orden.proveedor.nombre_proveedor if orden.proveedor else ''
            })
    
    paginator = Paginator(orden_all, num_elemento)  
    orden_list = paginator.get_page(page)
    template_name = 'orden/orden_lista_bloqueada.html'
    return render(request, template_name, {'profiles': profiles, 'orden_list': orden_list, 'paginator': paginator, 'page': page, 'search': search })
@login_required    
def proveedor_lista_bloqueado(request,page=None,search=None):
    profiles = Profile.objects.get(user_id = request.user.id)
    if profiles.group_id != 1 and profiles.group_id != 3:
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
    print("search> ",search)
    proveedor_all = [] #lista vacia para agrega la salida de la lista ya sea con la cadena de búsqueda o no
    if search == None or search == "None":# si la cadena de búsqueda viene vacia
        #usuario_count = proveedor.objects.filter(is_active='t').count()
        proveedor_array = Proveedor.objects.filter(estado_proveedor='f').order_by('nombre_proveedor')
        
        for pr in proveedor_array:
            #se guarda la información del usuario
            proveedor_all.append({'id':pr.id,'nombre_proveedor':pr.nombre_proveedor,'correo_proveedor':pr.correo_proveedor,'telefono_proveedor':pr.telefono_proveedor,'rut_proveedor':pr.rut_proveedor})
        paginator = Paginator(proveedor_all, num_elemento)  
        proveedor_list = paginator.get_page(page)
        template_name = 'proveedor/proveedor_lista_bloqueado.html'
        return render(request,template_name,{'profiles':profiles,'proveedor_list':proveedor_list,'paginator':paginator,'page':page,'search':search })
            
    else:#si la cadena de búsqueda trae datos
        #h_count = User.objects.filter(is_active='t').filter(nombre__icontains=search).count()
        #Lógica de busqueda por primer nombre, nombre de usuario, los filtra si están activos o no y se ordena por primer nombre de forma ascendente
        proveedor_array =  Proveedor.objects.filter(Q(nombre_proveedor__icontains=search)|Q(rut_proveedor__icontains=search)).filter(estado_proveedor='f').order_by('nombre_proveedor')#Ascendente
        
        for pr in proveedor_array:
            
            #se guarda la información del usuario
            proveedor_all.append({'id':pr.id,'nombre_proveedor':pr.nombre_proveedor,'correo_proveedor':pr.correo_proveedor,'telefono_proveedor':pr.telefono_proveedor,'rut_proveedor':pr.rut_proveedor})
            
    #user_array = User.objects.filter(is_active='t').order_by('nombre_proveedor')
    #profile_data = Profile.objects.all()
    paginator = Paginator(proveedor_all, num_elemento)  
    proveedor_list = paginator.get_page(page)
    template_name = 'proveedor/proveedor_lista_bloqueado.html'
    return render(request,template_name,{'profiles':profiles,'proveedor_list':proveedor_list,'paginator':paginator,'page':page ,'search':search })


@login_required
def proveedor_block(request,proveedor_id):
    profiles = Profile.objects.get(user_id = request.user.id)
    if profiles.group_id != 1 and profiles.group_id != 3:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')

    order_data_count = Proveedor.objects.filter(pk=proveedor_id).count()
    proveedor_data = Proveedor.objects.get(pk=proveedor_id)     
    if order_data_count == 1:
        Proveedor.objects.filter(pk=proveedor_id).update(estado_proveedor='f')
        messages.add_message(request, messages.INFO, 'Proveedor '+proveedor_data.nombre_proveedor +' bloqueado con éxito')
        return redirect('proveedor_lista_activo')        
    else:
        messages.add_message(request, messages.INFO, 'Hubo un error al bloquear el Proveedor '+proveedor_data.nombre_proveedor )
        return redirect('proveedor_lista_activo')    
@login_required
def proveedor_activate(request,proveedor_id):
    profiles = Profile.objects.get(user_id = request.user.id)
    if profiles.group_id != 1 and profiles.group_id != 3:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    proveedor_data_count = Proveedor.objects.filter(pk=proveedor_id).count()
    proveedor_data = Proveedor.objects.get(pk=proveedor_id)     
    if proveedor_data_count == 1:
        Proveedor.objects.filter(pk=proveedor_id).update(estado_proveedor='t')
        messages.add_message(request, messages.INFO, 'Proveedor '+proveedor_data.nombre_proveedor +' activado con éxito')
        return redirect('proveedor_lista_bloqueado')        
    else:
        messages.add_message(request, messages.INFO, 'Hubo un error al activar el Proveedor '+proveedor_data.nombre_proveedor)
        return redirect('proveedor_lista_bloqueado')        

@login_required
def proveedor_delete(request,proveedor_id):
    profiles = Profile.objects.get(user_id = request.user.id)
    if profiles.group_id != 1 and profiles.group_id != 3:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')

    proveedor_data_count = Proveedor.objects.filter(pk=proveedor_id).count()
    proveedor_data = Proveedor.objects.get(pk=proveedor_id)
   
    if proveedor_data_count == 1:
        #Profile.objects.filter(proveedor_id=proveedor_id).delete()
        Proveedor.objects.filter(pk=proveedor_id).delete()
        ProveedorDireccion.objects.filter(proveedor_id=proveedor_id).delete
        messages.add_message(request, messages.INFO, 'Proveedor '+proveedor_data.nombre_proveedor +' eliminado con éxito')
        return redirect('proveedor_lista_bloqueado')        
    else:
        messages.add_message(request, messages.INFO, 'Hubo un error al eliminar al Proveedor '+proveedor_data.nombre_proveedor)
        return redirect('proveedor_lista_bloqueado')        

@login_required
def direccion_delete(request,direccion_id,proveedor_id):
    profiles = Profile.objects.get(user_id = request.user.id)
    if profiles.group_id != 1 and profiles.group_id != 3:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')

    direccion_data_count = Direccion.objects.filter(pk=direccion_id).count()
    direccion_data = Direccion.objects.get(pk=direccion_id)

    if direccion_data_count == 1:
        #Profile.objects.filter(direccion_id=direccion_id).delete()
        Direccion.objects.filter(pk=direccion_id).delete()
        ProveedorDireccion.objects.filter(direccion_id=direccion_id).delete
        #messages.add_message(request, messages.INFO, 'direccion '+direccion_data.obtener_direccion +' eliminada con éxito')
        return redirect('edit_proveedor',proveedor_id)        
    else:
        #messages.add_message(request, messages.INFO, 'Hubo un error al eliminar la direcci[on] '+direccion_data.obtener_direccion)
        return redirect('edit_proveedor',proveedor_id)      
    
    

@login_required
def direccion_edit(request,direccion_id,proveedor_id):
    profiles = Profile.objects.get(user_id = request.user.id)
    if profiles.group_id != 1 and profiles.group_id != 3:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    if request.method=='POST':
        region= request.POST.get('region')
        
        comuna= request.POST.get('comuna')
        calle= request.POST.get('calle')
        numero= request.POST.get('numero')
        departamento= request.POST.get('departamento')
        piso= request.POST.get('piso')
        state=True
        validar = True
        direccion_data_count = Direccion.objects.filter(pk=direccion_id).count()
        direccion_data = Direccion.objects.get(pk=direccion_id)
        if validacion.validar_calle(calle)==False:
                messages.add_message(request, messages.INFO, 'Ingresado incorrectamente la calle')
                validar=False
        if validacion.validar_int(numero)==False:
                messages.add_message(request, messages.INFO, 'Ingresado incorrectamente el numero')
                validar=False
        if validacion.validar_depto(departamento)==False:
                messages.add_message(request, messages.INFO, 'Ingresado incorrectamente el dpt')
                validar=False
        if validacion.validar_piso(piso)==False:
                messages.add_message(request, messages.INFO, 'Ingresado incorrectamente el piso')
                validar=False
        if direccion_data_count == 1:
            if validar==True:

                Direccion.objects.filter(pk = direccion_id).update(nombre_calle = calle.capitalize())
                Direccion.objects.filter(pk = direccion_id).update(numero_direccion = numero)
                Direccion.objects.filter(pk = direccion_id).update(departamento = departamento)  
                Direccion.objects.filter(pk = direccion_id).update(piso = piso)    
                Direccion.objects.filter(pk = direccion_id).update(comuna_id = comuna)         
                messages.add_message(request,messages.INFO,'Dirección editada con exito')
                return redirect('edit_proveedor',proveedor_id)  
            
    direccion_data = Direccion.objects.get(pk=direccion_id)
    comuna = Comuna.objects.get(pk = direccion_data.comuna_id)
    region = Region.objects.get(pk = comuna.region_id )
    regiones = Region.objects.all()
    

    template_name = 'proveedor/direccion_edit.html'
    return render(request,template_name,{'direccion_data':direccion_data,'profiles':profiles, 'comuna':comuna,'region':region,'regiones':regiones,'proveedor_id':proveedor_id })
    
    
    
    