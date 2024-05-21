
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

# Create your views here.



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

# views.py


def load_comunas(request):
    region_id = request.GET.get('region_id')
    comunas = Comuna.objects.filter(region_id=region_id).all()
    return JsonResponse(list(comunas.values('id', 'nombre_comuna')), safe=False)


@login_required
def proveedor_save(request):

    if request.method=='POST':
        name= request.POST.get('name')
        region= request.POST.get('region')
        comuna= request.POST.get('comuna')
        calle= request.POST.get('calle')
        numero= request.POST.get('numero')
        mobile= request.POST.get('mobile')
        correo= request.POST.get('correo')
        departamento= request.POST.get('departamento')
        piso= request.POST.get('piso')
        state=True
        validar = True
        
        #proveedor_exist = peo.objects.filter(category_group_name=name).count()
        proveedor_exist = 0
        if proveedor_exist==1:
            validar=False
            messages.add_message(request,messages.INFO,'Solo puede haber un proveedor')
        if name=='':
            messages.add_message(request,messages.INFO,'Debe ingresar un nombre para el proveedor')
            return('proveedor_create')   
        #creo k es mejor k la validacion contemple todo, si esta vacio, si es el tipo de dato, etc
        """
        if validacion.validar_soloString(name)==False:
            validar=False
            messages.add_message(request,messages.INFO,'El nombre solo debe contener letras')
         """
        if validar==True:
            proveedor_save=Proveedor(
                nombre_proveedor=name,
                correo_proveedor=correo,
                telefono_proveedor=mobile,
                estado_proveedor="t",
            )
            proveedor_save.save()

            proveedorcalle_save = Calle (
                nombre_calle = calle,
                comuna_id = comuna ,
            )
            proveedorcalle_save.save()

            direccion_save = Direccion (
                numero_dirrecion = numero,
                calle_id = proveedorcalle_save.id,
                
                )
            direccion_save.save()
            
            proveedordireccion_save = ProveedorDireccion (

                direccion_id = direccion_save.id,
                proveedor_id = proveedor_save.id,
                departamento = departamento,
                piso = piso,
                
            )
            
            proveedordireccion_save.save()

            
            
            messages.add_message(request,messages.INFO,'Proveedor creado con exito')
    return redirect('proveedor_main')