
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
from proveedor.models import *
from django.http import JsonResponse
#validaciones .py!!!!! <---------------------------------
from extensiones import validacion
# Create your views here.
#numero de elementos para el listado
global num_elemento 
num_elemento = 1



@login_required
def proveedor_main(request):
    profiles = Profile.objects.get(user_id = request.user.id)
    if profiles.group_id != 1 and profiles.group_id != 3:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    template_name = 'proveedor/proveedor_main.html'
    return render(request,template_name,{'profiles':profiles})



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
        if name=='':
            messages.add_message(request,messages.INFO,'Debe ingresar un nombre para el proveedor')
            return('proveedor_create')  
        #es mejor k la validacion contemple todo, si esta vacio, si es el tipo de dato, etc
        """
        if validacion.validar_soloString(name)==False:
            validar=False
            messages.add_message(request,messages.INFO,'El nombre solo debe contener letras')
         """
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
    #groups = Group.objects.all().exclude(pk=0).order_by('id')
    
    if profiles.group_id != 1 and profiles.group_id != 3:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    
    template_name = 'proveedor/proveedor_lista_main.html'
    return render(request,template_name,{'profiles':profiles})



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
            if name is None:
                validar = False
            if rut is None:
                validar = False
            if mobile is None:
                validar = False
            if name is None:
                correo = False
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
        print("search 1 : ", search)
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

        print("search 2 : ", search)
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

    proveedor_data_count = Proveedor.objects.filter(pk=proveedor_id).count()
    proveedor_data = Proveedor.objects.get(pk=proveedor_id)     
    if proveedor_data_count == 1:
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
    