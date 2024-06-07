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
from carrito.Carrito import *
# Create your views here.
#numero de elementos para el listado
global num_elemento 
num_elemento = 30



@login_required
def venta_main(request):
    profiles = Profile.objects.get(user_id = request.user.id)
    if not(profiles.group_id == 1 or profiles.group_id == 4):
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    template_name = 'venta/venta_main.html'
    return render(request,template_name,{'profiles':profiles})

"""

def crear_venta(request):
    if request.method == 'POST':
        form = TuModeloForm(request.POST)
        if form.is_valid():
            nueva_venta = form.save(commit=False)
            nueva_venta.save()
            # Redirige o realiza otras acciones necesarias
    else:
        form = TuModeloForm()
    
    return render(request, 'tu_template.html', {'form': form})

"""



@login_required
def cliente_create(request):
    profiles = Profile.objects.get(user_id = request.user.id)
    if profiles.group_id != 1 and profiles.group_id != 4:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    template_name = 'venta/cliente_create.html'
    category_group_data = Category_group.objects.all()
    return render(request,template_name,{'category_groups':category_group_data})
@login_required
def cliente_save(request):
    profiles = Profile.objects.get(user_id = request.user.id)
    if profiles.group_id != 1 and profiles.group_id != 3:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')

    if request.method == 'POST':
        
        validar=True
        rut = request.POST.get('rut')
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        rut_exist = Cliente.objects.filter(rut_cliente=rut).count()
        mail_exist = Cliente.objects.filter(correo_cliente=email).count()
        #cambie toda la estructura pero no me gusta tanto (ineficiente)

        if validacion.validar_soloString(nombre)==False: #<- de validaciones Strings
            validar=False
            messages.add_message(request, messages.INFO, 'Error en Nombre: invalido')  
        if validacion.validar_soloString(apellido)==False: #<- de validaciones Strings
            validar=False
            messages.add_message(request, messages.INFO, 'Error en Apellido: invalido')

        if validacion.validar_numCelular(mobile)==False:
            validar=False
            messages.add_message(request, messages.INFO, 'Error en numero de telefono: Ingrese un numero telefonico valido')#Buscar regeex numero chilenos
        #Posiblemente unificar los if con "&", PERO CAMBIAR LOS MENSAJES ELSE/ O QUIZAS CREAR UNA NUEVA FUNCION.<-----
        if validacion.validar_rut(rut)==False: #<- de validaciones saca validar_rut
                    messages.add_message(request, messages.INFO, 'Rut invalido')  
                    validar=False

        if validacion.validar_email(email)==False: #<- de validaciones saca validar_email
                    messages.add_message(request, messages.INFO, 'Email invalido')  
                    validar=False
        if rut_exist==1:
                messages.add_message(request, messages.INFO, 'Rut ya esta registrado')
                validar=False

        if mail_exist==1:
                messages.add_message(request, messages.INFO, 'Este correo ya esta registrado')  
                validar=False
        if validar == True:
                    cliente = Cliente(
                        rut_cliente= rut,
                        nombre_cliente=nombre.capitalize(),#hace que el primero sea mayuscula (.capitalize())
                        apellido_cliente=apellido.capitalize(),#hace que el primero sea mayuscula (.capitalize())
                        correo_cliente=email,
                        telefono_cliente = mobile,
                        estado_cliente = 't',
                    
                        )
                    cliente.save()
                    messages.add_message(request, messages.INFO, 'Cliente creado con exito')                             

        #el metodo no contempla validacioens deberá realizarlas
    
    return redirect('venta_main')



def cliente_lista_principal(request):
    profiles = Profile.objects.get(user_id = request.user.id)
    #groups = Group.objects.all().exclude(pk=0).order_by('id')
    
    if profiles.group_id != 1 and profiles.group_id != 4:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    
    template_name = 'venta/cliente_lista_principal.html'
    return render(request,template_name,{'profiles':profiles})


@login_required
def edit_cliente(request,cliente_id):
    profiles = Profile.objects.get(user_id = request.user.id)
    validar = True
    if profiles.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    if request.method == 'POST':
        rut = request.POST.get('rut')
        cliente_id = request.POST.get('cliente_id')
        nombre_cliente = request.POST.get('nombre')
        apellido_cliente = request.POST.get('apellido')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        
        cliente_data_count = Cliente.objects.filter(pk=cliente_id).count()
        cliente_data = Cliente.objects.get(pk=cliente_id)

        if cliente_data_count == 1:
            #CUMPLE CON LA FORMA DE UN EMAIL
            if validacion.validar_email(email)==False:
                validar=False
            #SOLO STRING
            if validacion.validar_soloString(nombre_cliente)== False:
                validar=False
            if validacion.validar_soloString(apellido_cliente)== False:
                validar=False
            #si el correo existe
            if cliente_data.correo_cliente != email:
                cliente_mail_count_all = Cliente.objects.filter(email=email).count()
                if cliente_mail_count_all > 0:
                    #que es page
                    messages.add_message(request, messages.INFO, 'El correo '+str(email)+' ya existe en nuestros registros asociado a otro Cliente, por favor utilice otro ')       
                    return redirect('cliente_listado_activo',page)
            #Si se cumple Todas las especificaciones lleva aca -Enzo
            if validar == True:
                Cliente.objects.filter(pk = cliente_id).update(rut_cliente = rut)   
                Cliente.objects.filter(pk = cliente_id).update(nombre_cliente = nombre_cliente.capitalize())
                Cliente.objects.filter(pk = cliente_id).update(apellido_cliente = apellido_cliente.capitalize())  
                Cliente.objects.filter(pk = cliente_id).update(correo_cliente = email)    
                Cliente.objects.filter(pk = cliente_id).update(telefono_cliente = mobile)           
                messages.add_message(request, messages.INFO, f"Cliente {cliente_data.nombre_completo()} editado con exito")                             
                return redirect('cliente_lista_activo')
            #Si no se cumple alguna de las especificaciones lleva aca -Enzo
            else:
                messages.add_message(request, messages.INFO, 'Complete segun lo pedido') 
                #que es page                            
                return redirect('cliente_lista_activo',page)
        else:
            messages.add_message(request, messages.INFO, f"Hubo un error al editar al Cliente {cliente_data.nombre_completo()} ")
            return redirect('cliente_lista_activo')    
    cliente_data = Cliente.objects.get(pk=cliente_id) 
    template_name = 'venta/edit_cliente.html'
    return render(request,template_name,{'cliente_data':cliente_data})
@login_required
def ver_cliente(request, cliente_id):
    profiles = Profile.objects.get(user_id=request.user.id)
    if profiles.group_id != 1 and profiles.group_id != 2:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main') 
    template_name = 'venta/ver_cliente.html'
    cliente_data = Cliente.objects.get(pk=cliente_id)
    return render(request,template_name,{'cliente_data':cliente_data})

@login_required    
def cliente_lista_activo(request,page=None,search=None):
    profiles = Profile.objects.get(user_id = request.user.id)
    if profiles.group_id != 1 and profiles.group_id != 4:
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
    cliente_all = [] #lista vacia para agrega la salida de la lista ya sea con la cadena de búsqueda o no
    if search == None or search == "None":# si la cadena de búsqueda viene vacia
        #usuario_count = cliente.objects.filter(estado_cliente='t').count()
        cliente_array = Cliente.objects.filter(estado_cliente='t').order_by('nombre_cliente')
        
        for cl in cliente_array:
            #se guarda la información del cluario
        
            cliente_all.append({'id':cl.id,'rut_cliente':cl.rut_cliente,'nombre_cliente':cl.nombre_completo(),'correo_cliente':cl.correo_cliente,'telefono_cliente':cl.telefono_cliente})
        paginator = Paginator(cliente_all, num_elemento)  
        cliente_list = paginator.get_page(page)
        template_name = 'venta/cliente_lista_activo.html'
        return render(request,template_name,{'profiles':profiles,'cliente_list':cliente_list,'paginator':paginator,'page':page,'search':search })
            
    else:#si la cadena de búsqueda trae datos
        #h_count = cliente.objects.filter(estado_cliente='t').filter(nombre__icontains=search).count()
        #Lógica de busqueda por primer nombre, nombre de usuario, los filtra si están activos o no y se ordena por primer nombre de forma ascendente
        cliente_array =  Cliente.objects.filter(Q(nombre_cliente__icontains=search)|Q(rut_cliente__icontains=search)).filter(estado_cliente='t').order_by('nombre_cliente')#Ascendente
        
        for cl in cliente_array:
            #se guarda la información del cluario
        
            cliente_all.append({'id':cl.id,'rut_cliente': cl.rut_cliente,'nombre_cliente':cl.nombre_completo(),'correo_cliente':cl.correo_cliente,'telefono_cliente':cl.telefono_cliente})
        paginator = Paginator(cliente_all, num_elemento)            

    paginator = Paginator(cliente_all, num_elemento)  
    cliente_list = paginator.get_page(page)
    template_name = 'venta/cliente_lista_activo.html'
    return render(request,template_name,{'profiles':profiles,'cliente_list':cliente_list,'paginator':paginator,'page':page ,'search':search })

@login_required    
def cliente_lista_bloqueado(request,page=None,search=None):
    
    profiles = Profile.objects.get(user_id = request.user.id)
    if profiles.group_id != 1 and profiles.group_id != 4:
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
    cliente_all = [] #lista vacia para agrega la salida de la lista ya sea con la cadena de búsqueda o no
    if search == None or search == "None":# si la cadena de búsqueda viene vacia
        #usuario_count = cliente.objects.filter(estado_cliente='t').count()
        cliente_array = Cliente.objects.filter(estado_cliente='f').order_by('nombre_cliente')
        
        for cl in cliente_array:
            #se guarda la información del cluario
        
            cliente_all.append({'id':cl.id,'rut_cliente':cl.rut_cliente,'nombre_cliente':cl.nombre_completo(),'correo_cliente':cl.correo_cliente,'telefono_cliente':cl.telefono_cliente})
        paginator = Paginator(cliente_all, num_elemento)  
        cliente_list = paginator.get_page(page)
        template_name = 'venta/cliente_lista_bloqueado.html'
        return render(request,template_name,{'profiles':profiles,'cliente_list':cliente_list,'paginator':paginator,'page':page,'search':search })
            
    else:#si la cadena de búsqueda trae datos
        #h_count = cliente.objects.filter(estado_cliente='t').filter(nombre__icontains=search).count()
        #Lógica de busqueda por primer nombre, nombre de usuario, los filtra si están activos o no y se ordena por primer nombre de forma ascendente
        cliente_array =  Cliente.objects.filter(Q(nombre_cliente__icontains=search)|Q(rut_cliente__icontains=search)).filter(estado_cliente='f').order_by('nombre_cliente')#Ascendente
        
        for cl in cliente_array:
            #se guarda la información del cluario
        
            cliente_all.append({'id':cl.id,'rut_cliente':cl.rut_cliente,'nombre_cliente':cl.nombre_completo(),'correo_cliente':cl.correo_cliente,'telefono_cliente':cl.telefono_cliente})
        paginator = Paginator(cliente_all, num_elemento)            

    paginator = Paginator(cliente_all, num_elemento)  
    cliente_list = paginator.get_page(page)
    template_name = 'venta/cliente_lista_bloqueado.html'
    return render(request,template_name,{'profiles':profiles,'cliente_list':cliente_list,'paginator':paginator,'page':page ,'search':search })


@login_required
def cliente_block(request,cliente_id):
    profiles = Profile.objects.get(user_id = request.user.id)
    if profiles.group_id != 1 and profiles.group_id != 3:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')

    cliente_data_count = Cliente.objects.filter(pk=cliente_id).count()
    cliente_data = Cliente.objects.get(pk=cliente_id)
    if cliente_data_count == 1:
        Cliente.objects.filter(pk=cliente_id).update(estado_cliente='f')
        messages.add_message(request, messages.INFO, f"Cliente{cliente_data.nombre_completo()} bloqueado con éxito")
        return redirect('cliente_lista_activo')        
    else:
        messages.add_message(request, messages.INFO, f"Hubo un error al bloquear al Cliente {cliente_data.nombre_completo()} ")
        return redirect('cliente_lista_activo')        
@login_required
def cliente_activate(request,cliente_id):
    profiles = Profile.objects.get(user_id = request.user.id)
    if profiles.group_id != 1 and profiles.group_id != 3:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')

    cliente_data_count = Cliente.objects.filter(pk=cliente_id).count()
    cliente_data = Cliente.objects.get(pk=cliente_id)
    if cliente_data_count == 1:
        Cliente.objects.filter(pk=cliente_id).update(estado_cliente='t')
        messages.add_message(request, messages.INFO, f"Cliente{cliente_data.nombre_completo()} Activado con éxito")
        return redirect('cliente_lista_bloqueado')        
    else:
        messages.add_message(request, messages.INFO, f"Hubo un error al Activar al Cliente {cliente_data.nombre_completo()} ")
        return redirect('cliente_lista_bloqueado')           
    
@login_required
def cliente_delete(request,cliente_id):
    profiles = Profile.objects.get(user_id = request.user.id)
    if profiles.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')

    cliente_data_count = Cliente.objects.filter(pk=cliente_id).count()
    cliente_data = Cliente.objects.get(pk=cliente_id)
    if cliente_data_count == 1:
        #Profile.objects.filter(cliente_id=cliente_id).delete()

        Cliente.objects.filter(pk=cliente_id).delete()
        messages.add_message(request, messages.INFO, f"Cliente{cliente_data.nombre_completo()} Eliminado con éxito")
        return redirect('cliente_lista_bloqueado')        
    else:
        messages.add_message(request, messages.INFO, f"Hubo un error al Eliminar al Cliente {cliente_data.nombre_completo()} ")
        return redirect('cliente_lista_bloqueado')       


def finalizar_venta(request,cliente_id):
    carrito = Carrito(request)
    if carrito.esta_vacio():
        messages.error(request, 'El carrito está vacío.')
        return redirect('tienda')      

    # Verificar si el cliente y el método de pago existen
    try:
        cliente = Cliente.objects.get(id=cliente_id)
        
    except (Cliente.DoesNotExist):
        messages.error(request, 'Cliente  no válido.')
        return redirect('tienda')
    carrito = request.session.get('carrito', {})
    # Procesar los productos del carrito y calcular el total de la venta
    total_venta = 0
    venta = Venta(
        cliente=cliente,
        total_venta=total_venta, 
    )
    venta.save()
    for producto_id, detalle in carrito.items():
        producto = Producto.objects.get(id=detalle['producto_id'])
        cantidad = detalle['cantidad']
        print(f"stock: {producto.stock_producto}")
        print(f"cantidad: {cantidad}")
        if  cantidad <=  producto.stock_producto:
            producto_stock_update = producto.stock_producto - cantidad
            Producto.objects.filter(pk= producto_id).update(stock_producto = producto_stock_update)
        
            total_producto = detalle['acumulado']
            total_venta += total_producto

            # Guardar los detalles de la venta en la base de datos
            detalle_venta = VentaProducto(
                producto_id=producto.id,
                venta_id = venta.id,
                cantidad = cantidad,
                #cantidad=cantidad,
                #precio_unitario=producto.precio_producto,
                #total=total_producto
            )
            detalle_venta.save()
        else:
            messages.add_message(request, messages.INFO, f'No hay stock suficiente para el producto: {producto.nombre_producto}')
            return redirect('tienda')
    # Crear una nueva instancia de Venta
    Venta.objects.filter(id=venta.id).update(total_venta=total_venta)

    # Asociar los productos vendidos a la venta
    #venta.venta_producto.set(VentaProducto.objects.all())

    # Limpiar el carrito después de procesar la venta
    request.session['carrito'] = {}

    # Redirigir a la página de confirmación con un mensaje
    messages.success(request, 'La venta se ha procesado correctamente.')
    return redirect('tienda')



@login_required    
def cliente_lista_venta(request,cliente_id,page=None,search=None):
    
    profiles = Profile.objects.get(user_id = request.user.id)
    if profiles.group_id != 1 and profiles.group_id != 4:
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

    venta_all = [] #lista vacia para agrega la salida de la lista ya sea con la cadena de búsqueda o no
    if search == None or search == "None":# si la cadena de búsqueda viene vacia
        #usuario_count = cliente.objects.filter(estado_cliente='t').count()
        venta_array =  Venta.objects.filter(cliente_id = cliente_id).order_by('formatted_codigo_venta')
        
        for cl in venta_array:
            #se guarda la información de la venta
            venta_all.append({'id':cl.id,'creacion_venta':cl.creacion_venta,'total_venta':cl.total_venta,'codigo_venta':cl.formatted_codigo_venta})
        paginator = Paginator(venta_all, num_elemento)  
        venta_list = paginator.get_page(page)
        template_name = 'venta/cliente_lista_venta.html'
        return render(request,template_name,{'profiles':profiles,'venta_list':venta_list,'paginator':paginator,'page':page,'search':search })
            
    else:#si la cadena de búsqueda trae datos
        #h_count = cliente.objects.filter(estado_cliente='t').filter(nombre__icontains=search).count()
        #Lógica de busqueda por primer nombre, nombre de usuario, los filtra si están activos o no y se ordena por primer nombre de forma ascendente
        venta_array =  Venta.objects.filter(Q(formatted_codigo_venta__icontains=search)).filter(cliente_id = cliente_id).order_by('formatted_codigo_venta')#Ascendente
        
        for cl in venta_array:
            #se guarda la información del cluario
        
            venta_all.append({'id':cl.id,'creacion_venta': cl.creacion_venta,'total_venta':cl.total_venta,'codigo_venta':cl.formatted_codigo_venta})
        paginator = Paginator(venta_all, num_elemento)            

    paginator = Paginator(venta_all, num_elemento)  
    venta_list = paginator.get_page(page)
    template_name = 'venta/cliente_lista_venta.html'
    return render(request,template_name,{'profiles':profiles,'venta_list':venta_list,'paginator':paginator,'page':page ,'search':search })

@login_required    
def cliente_lista_venta_detalle(request,venta_id,page=None,search=None):
    
    profiles = Profile.objects.get(user_id = request.user.id)
    if profiles.group_id != 1 and profiles.group_id != 4:
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
    ventaC =  Venta.objects.get(pk = venta_id)
    
    clientes = Cliente.objects.filter(pk = ventaC.cliente_id)
    for c in clientes:
        cliente_id = c.id
    venta_all = [] #lista vacia para agrega la salida de la lista ya sea con la cadena de búsqueda o no
    if search == None or search == "None" or search == "":# si la cadena de búsqueda viene vacia
        #usuario_count = cliente.objects.filter(estado_cliente='t').count()
        venta_array =  VentaProducto.objects.filter(venta_id = venta_id).order_by('venta_id')
        
        for cl in venta_array:
            #se guarda la información de la venta
            nombre_producto = Producto.objects.get(pk = cl.producto_id).nombre_producto
            venta_all.append({'nombre':nombre_producto,'cantidad':cl.cantidad,'precio_unitario':cl.precio_unitario, 'precio_total':cl.precio_total})
        paginator = Paginator(venta_all, num_elemento)  
        venta_detalle_list = paginator.get_page(page)
        template_name = 'venta/cliente_lista_venta_detalle.html'
        return render(request,template_name,{'profiles':profiles,'venta_detalle_list':venta_detalle_list,'cliente':cliente_id,'paginator':paginator,'page':page,'search':search })
            
    else:#si la cadena de búsqueda trae datos
        #h_count = cliente.objects.filter(estado_cliente='t').filter(nombre__icontains=search).count()
        #Lógica de busqueda por primer nombre, nombre de usuario, los filtra si están activos o no y se ordena por primer nombre de forma ascendente
        productos = Producto.objects.filter(Q(nombre_producto__icontains=search))
            
        for producto in productos:
            # Filtrar los productos vendidos en esta venta
            venta_array = VentaProducto.objects.filter(
                Q(producto_id=producto.id), Q(venta_id=venta_id)
            ).order_by('venta_id')
        
            for cl in venta_array:
                #se guarda la información de la venta
                nombre_producto = Producto.objects.get(pk = cl.producto_id).nombre_producto
                venta_all.append({'nombre':nombre_producto,'cantidad':cl.cantidad,'precio_unitario':cl.precio_unitario, 'precio_total':cl.precio_total})

    paginator = Paginator(venta_all, num_elemento)  
    venta_detalle_list = paginator.get_page(page)
    template_name = 'venta/cliente_lista_venta_detalle.html'
    return render(request,template_name,{'profiles':profiles,'venta_detalle_list':venta_detalle_list,'cliente':cliente_id,'paginator':paginator,'page':page ,'search':search })





