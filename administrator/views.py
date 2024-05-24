import calendar
import json
import random
from turtle import home
import pandas as pd
from datetime import datetime, time, timedelta
from django.utils import timezone
from datetime import datetime
import pytz

import xlwt

from django.http import HttpResponse
from django import forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, GroupManager, User
from django.core.mail import EmailMultiAlternatives
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Avg, Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from dateutil import relativedelta
from registration.models import Profile

#validaciones .py!!!!! <---------------------------------
from extensiones import validacion
global num_elemento 
num_elemento = 2
@login_required
def admin_main(request):
    profiles = Profile.objects.get(user_id = request.user.id)
    if profiles.group_id != 1 and profiles.group_id != 2:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    template_name = 'administrator/admin_main.html'
    return render(request,template_name,{'profiles':profiles})

#Flujo usuarios
@login_required
def users_main(request):
    profiles = Profile.objects.get(user_id = request.user.id)
    if profiles.group_id != 1 and profiles.group_id != 2:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    groups = Group.objects.all().exclude(pk=0).order_by('id')
    template_name = 'administrator/users_main.html'
    return render(request,template_name,{'groups':groups,'profiles':profiles})

@login_required
def new_user(request):
    profiles = Profile.objects.get(user_id = request.user.id)
    if profiles.group_id != 1:
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
    if request.method == 'POST':
        
        validar=True

        grupo = request.POST.get('grupo')
        rut = request.POST.get('rut')
        first_name = request.POST.get('name')
        last_name = request.POST.get('last_name1')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        cargo = request.POST.get('position')

        rut_exist = User.objects.filter(username=rut).count()
        mail_exist = User.objects.filter(email=email).count()
        print (mail_exist)
        #cambie toda la estructura pero no me gusta tanto (ineficiente)

        if validacion.validar_soloString(first_name)==False: #<- de validaciones Strings
            validar=False
            messages.add_message(request, messages.INFO, 'Error en Nombre: invalido')  
        if validacion.validar_soloString(last_name)==False: #<- de validaciones Strings
            validar=False
            messages.add_message(request, messages.INFO, 'Error en Apellido: invalido')
        if validacion.validar_soloString(cargo)==False: #<- de validaciones Strings
            validar=False                               #cargo     QUIZAS SE VA
            messages.add_message(request, messages.INFO, 'Error en cargo: invalido')

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
                    user = User.objects.create_user(
                        username= rut,
                        email=email,
                        password=rut,
                        first_name=first_name.capitalize(),#hace que el primero sea mayuscula (.capitalize())
                        last_name=last_name.capitalize()#hace que el primero sea mayuscula (.capitalize())
                        )
                    profile_save = Profile(
                        user_id = user.id,
                        group_id = grupo,
                        first_session = 'Si',
                        token_app_session = 'No',
                        )
                    profile_save.save()
                    messages.add_message(request, messages.INFO, 'Usuario creado con exito')                             
 
        #el metodo no contempla validacioens deberá realizarlas
    groups = Group.objects.all().exclude(pk=0).order_by('id')
    template_name = 'administrator/new_user.html'
    return render(request,template_name,{'groups':groups})

def list_main2(request):
    profiles = Profile.objects.get(user_id = request.user.id)
    #groups = Group.objects.all().exclude(pk=0).order_by('id')
    
    if profiles.group_id != 1 and profiles.group_id != 2:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    
    template_name = 'administrator/list_main2.html'
    return render(request,template_name,{'profiles':profiles})


@login_required
def edit_user(request,user_id):
    profiles = Profile.objects.get(user_id = request.user.id)
    validar = True
    if profiles.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    if request.method == 'POST':
        grupo = request.POST.get('grupo')
        user_id = request.POST.get('user_id')
        first_name = request.POST.get('name')
        last_name = request.POST.get('last_name1')
        email = request.POST.get('email')
        group = request.POST.get('group')
        user_data_count = User.objects.filter(pk=user_id).count()
        user_data = User.objects.get(pk=user_id)
        profile_data = Profile.objects.get(user_id=user_id)

        if user_data_count == 1:
            #CUMPLE CON LA FORMA DE UN EMAIL
            if validacion.validar_email(email)==False:
                validar=False
            #SOLO STRING
            if validacion.validar_soloString(first_name)== False:
                validar=False
            if validacion.validar_soloString(last_name)== False:
                validar=False
            #si el correo existe
            if user_data.email != email:
                user_mail_count_all = User.objects.filter(email=email).count()
                if user_mail_count_all > 0:
                    #que es page
                    messages.add_message(request, messages.INFO, 'El correo '+str(email)+' ya existe en nuestros registros asociado a otro usuario, por favor utilice otro ')       
                    return redirect('list_user_active2',page)
            #Si se cumple Todas las especificaciones lleva aca -Enzo
            if validar == True:
                User.objects.filter(pk = user_id).update(first_name = first_name.capitalize())
                User.objects.filter(pk = user_id).update(last_name = last_name.capitalize())  
                User.objects.filter(pk = user_id).update(email = email)
                Profile.objects.filter(user_id = user_id).update(group_id = group)                
                messages.add_message(request, messages.INFO, 'Usuario '+user_data.first_name +' '+user_data.last_name+' editado con éxito')                             
                return redirect('list_user_active2')
            #Si no se cumple alguna de las especificaciones lleva aca -Enzo
            else:
                messages.add_message(request, messages.INFO, 'Complete segun lo pedido') 
                #que es page                            
                return redirect('list_user_active2',page)
        else:
            messages.add_message(request, messages.INFO, 'Hubo un error al editar el Usuario '+user_data.first_name +' '+user_data.last_name)
            return redirect('list_user_active2')    
    user_data = User.objects.get(pk=user_id)
    profile_data = Profile.objects.get(user_id=user_id)
    groups = Group.objects.get(pk=profile_data.group_id) 

    profile_list = Group.objects.all().exclude(pk=0).order_by('name')    
    template_name = 'administrator/edit_user.html'
    return render(request,template_name,{'user_data':user_data,'profile_data':profile_data,'groups':groups,'profile_list':profile_list})

@login_required    
def list_user_active2(request,page=None,search=None):
    profiles = Profile.objects.get(user_id = request.user.id)
    if profiles.group_id != 1 and profiles.group_id != 2:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    
    #fin logica que permite recibir la cadena de búsqueda y propoga a través del paginador
    print("search> ",search)
    user_all = [] #lista vacia para agrega la salida de la lista ya sea con la cadena de búsqueda o no
    if search == None or search == "None":# si la cadena de búsqueda viene vacia
        #usuario_count = User.objects.filter(is_active='t').count()
        user_array = User.objects.filter(is_active='t').order_by('first_name')
        
        for us in user_array:
            profile_data = Profile.objects.get(user_id=us.id)
            profile = profile_data.group
            name = us.first_name+' '+us.last_name
            #se guarda la información del usuario
            user_all.append({'id':us.id,'user_name':us.username,'name':name,'mail':us.email, 'profile':profile})
        paginator = Paginator(user_all, num_elemento)  
        user_list = paginator.get_page(page)
        template_name = 'administrator/list_user_active2.html'
        return render(request,template_name,{'profiles':profiles,'user_list':user_list,'paginator':paginator,'page':page,'search':search })
            
    else:#si la cadena de búsqueda trae datos
        #h_count = User.objects.filter(is_active='t').filter(nombre__icontains=search).count()
        #Lógica de busqueda por primer nombre, nombre de usuario, los filtra si están activos o no y se ordena por primer nombre de forma ascendente
        user_array =  User.objects.filter(Q(first_name__icontains=search)|Q(username__icontains=search)).filter(is_active='t').order_by('first_name')#Ascendente
        
        for us in user_array:
            profile_data = Profile.objects.get(user_id=us.id)
            profile = profile_data.group
            name = us.first_name+' '+us.last_name
            #se guarda la información del usuario
            user_all.append({'id':us.id,'user_name':us.username,'name':name,'mail':us.email, 'profile':profile})            
    
    #user_array = User.objects.filter(is_active='t').order_by('first_name')
    #profile_data = Profile.objects.all()
    paginator = Paginator(user_all, num_elemento)  
    user_list = paginator.get_page(page)
    template_name = 'administrator/list_user_active2.html'
    return render(request,template_name,{'profiles':profiles,'user_list':user_list,'paginator':paginator,'page':page ,'search':search })

@login_required    
def list_user_block2(request,page=None,search=None):
    
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
    user_all = [] #lista vacia para agrega la salida de la lista ya sea con la cadena de búsqueda o no
    if search == None or search == "None":# si la cadena de búsqueda viene vacia
        #usuario_count = User.objects.filter(is_active='f').count()
        user_array = User.objects.filter(is_active='f').order_by('first_name')
        
        for us in user_array:
            profile_data = Profile.objects.get(user_id=us.id)
            profile = profile_data.group
            name = us.first_name+' '+us.last_name
            #se guarda la información del usuario
            user_all.append({'id':us.id,'user_name':us.username,'name':name,'mail':us.email, 'profile':profile})
        paginator = Paginator(user_all, num_elemento)  
        user_list = paginator.get_page(page)
        template_name = 'administrator/list_user_block2.html'
        return render(request,template_name,{'profiles':profiles,'user_list':user_list,'paginator':paginator,'page':page,'search':search })
    else:#si la cadena de búsqueda trae datos
        #h_count = User.objects.filter(is_active='t').filter(nombre__icontains=search).count()
        #Lógica de busqueda por primer nombre, nombre de usuario, los filtra si están inactivos y se ordena por primer nombre de forma ascendente
        user_array =  User.objects.filter(Q(first_name__icontains=search)|Q(username__icontains=search)).filter(is_active='f').order_by('first_name')#Ascendente
        
        for us in user_array:
            profile_data = Profile.objects.get(user_id=us.id)
            profile = profile_data.group
            name = us.first_name+' '+us.last_name
            #se guarda la información del usuario
            user_all.append({'id':us.id,'user_name':us.username,'name':name,'mail':us.email, 'profile':profile})            
    
    #profile_data = Profile.objects.all()
    paginator = Paginator(user_all, num_elemento)  
    user_list = paginator.get_page(page)
    template_name = 'administrator/list_user_block2.html'
    return render(request,template_name,{'profiles':profiles,'user_list':user_list,'paginator':paginator,'page':page ,'search':search})


@login_required
def user_block(request,user_id):
    profiles = Profile.objects.get(user_id = request.user.id)
    if profiles.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')

    user_data_count = User.objects.filter(pk=user_id).count()
    user_data = User.objects.get(pk=user_id)
    profile_data = Profile.objects.get(user_id=user_id)       
    if user_data_count == 1:
        User.objects.filter(pk=user_id).update(is_active='f')
        messages.add_message(request, messages.INFO, 'Usuario '+user_data.first_name +' '+user_data.last_name+' bloqueado con éxito')
        return redirect('list_user_active2')        
    else:
        messages.add_message(request, messages.INFO, 'Hubo un error al bloquear el Usuario '+user_data.first_name +' '+user_data.last_name)
        return redirect('list_user_active2')        
@login_required
def user_activate(request,user_id):
    profiles = Profile.objects.get(user_id = request.user.id)
    if profiles.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    user_data_count = User.objects.filter(pk=user_id).count()
    user_data = User.objects.get(pk=user_id)
    profile_data = Profile.objects.get(user_id=user_id)       
    if user_data_count == 1:
        User.objects.filter(pk=user_id).update(is_active='t')
        messages.add_message(request, messages.INFO, 'Usuario '+user_data.first_name +' '+user_data.last_name+' activado con éxito')
        return redirect('list_user_block2')        
    else:
        messages.add_message(request, messages.INFO, 'Hubo un error al activar el Usuario '+user_data.first_name +' '+user_data.last_name)
        return redirect('list_user_block2')        

@login_required
def user_delete(request,user_id):
    profiles = Profile.objects.get(user_id = request.user.id)
    if profiles.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')

    user_data_count = User.objects.filter(pk=user_id).count()
    user_data = User.objects.get(pk=user_id)
    profile_data = Profile.objects.get(user_id=user_id)       
    if user_data_count == 1:
        #Profile.objects.filter(user_id=user_id).delete()
        Profile.objects.filter(user_id=user_id).delete()
        User.objects.filter(pk=user_id).delete()
        messages.add_message(request, messages.INFO, 'Usuario '+user_data.first_name +' '+user_data.last_name+' eliminado con éxito')
        return redirect('list_user_block2')        
    else:
        messages.add_message(request, messages.INFO, 'Hubo un error al eliminar el Usuario '+user_data.first_name +' '+user_data.last_name)
        return redirect('list_user_block2')        

def ejemplo_query_set(request):
    #los query set que estan acontinuación retornan elementos iterables
    #para obtener todos los datos de un modelo
    user_array =  User.objects.all()
    #para obtener todos los datos de un modelo ordenados por algún criterio
    user_array =  User.objects.all().order_by('username') #Ascendente
    user_array =  User.objects.all().order_by('-username') #Descendente
    #para obtener todos los datos de un modelo filtrado por algún criterio
    #para obtener todos los datos de un modelo excluyendo en base a algún criterio
    user_array =  User.objects.all().exclude(username='1234567')
    #si el criterio no existe retornará una lista vacia
    user_array =  User.objects.filter(username='1234567')  
    user_array =  User.objects.filter(username='1234567').order_by('username')#Ascendente
    user_array =  User.objects.filter(username='1234567').order_by('-username')#Descendente
    #para obtener todos los datos de un modelo filtrado por mas de un criterio
    user_array =  User.objects.filter(username='1234567').filter(is_active='t')  
    user_array =  User.objects.filter(username='1234567').filter(is_active='t').order_by('username')#Ascendente
    user_array =  User.objects.filter(username='1234567').filter(is_active='t').order_by('-username')#Descendente
    #para obtener todos los datos de un modelo filtrado por un criterio u otro
    #para usar el o debe importarlo al inicio del archivo from django.db.models Q
    user_array =  User.objects.filter(Q(username='1234567')|Q(is_active='t'))  
    user_array =  User.objects.filter(Q(username='1234567')|Q(is_active='t')).order_by('username')#Ascendente
    user_array =  User.objects.filter(Q(username='1234567')|Q(is_active='t')).order_by('-username')#Descendente

    #para obtener un solo registro
    '''
    si bien se suele usar con el id (pk), se pueden usar con cualquier otro criterio, de usarlo de esta forma debe 
    estar seguro de que le retornará un solo registro, ya que caso contrario le arrojará un error
    '''
    user_data = User.objects.get(pk=1)
    #si desea usar con otro criterio distinto a comparar con pk 
    user_data = User.objects.filter(is_active='t').first()#retorna el primer elemento de la lista
    #para actualizar registros
    User.objects.filter(pk=1).update(is_active='f')#actualiza el registro asociado al id
    User.objects.filter(is_active='f').update(is_active='t')#actualiza todos los registros que cumplen con el criterio
    #para contar registros
    user_data_count = User.objects.filter(pk=1).count()
    #la creación de registros la abordaremos más adelante


    print(user_data_count)
    return redirect('login')
"""def update_hours(request):
    profiles = Profile.objects.get(user_id = request.user.id)
    user_data = User.objects.get(pk=profiles.user_id)
    User.objects.filter(pk=profiles.user_id).update(horas_trabajadas='55')
    return redirect('login')"""
"""def update_hours(request):
    profiles = Profile.objects.get(user_id = request.user.id)
    user_data = User.objects.get(pk=profiles.user_id)
    last_login=user_data.last_login
    fecha_hora = timezone.datetime.strptime(str(last_login), "%Y-%m-%d %H:%M:%S.%f%z")
    hora_exacta1 = int(fecha_hora.strftime("%H"))
    hora_actual = datetime.now()
    hora_exacta = int(hora_actual.strftime("%H"))
    horas_trabajadas=abs(hora_exacta-hora_exacta1)
    Profile.objects.filter(pk=profiles.user_id).update(horas_trabajadas=int(hora_exacta))
    return redirect('login')    """

def update_hours(request):
    chile_tz = pytz.timezone('Chile/Continental')
    profiles = Profile.objects.get(user_id=request.user.id)
    user_data = profiles.user
    last_login = user_data.last_login
    fecha_hora = timezone.datetime.strptime(str(last_login), "%Y-%m-%d %H:%M:%S.%f%z")
    last_login_chile = fecha_hora.replace(tzinfo=pytz.utc).astimezone(chile_tz)
    hora_exacta1 = int(last_login_chile.strftime("%H"))
    hora_exacta_dia = int(last_login_chile.strftime("%d"))
    
    hora_actual = datetime.now()
    hora_actual_dia = int(hora_actual.strftime("%d"))
    hora_exacta = int(hora_actual.strftime("%H"))
    
    if hora_exacta_dia != hora_actual_dia:
        hora_exacta = abs(hora_exacta - 24)  # Ajuste para calcular correctamente las horas trabajadas si cambia el día
        horas_trabajadas2 = hora_exacta + hora_exacta1
    else:
        horas_trabajadas2 = abs(hora_exacta - hora_exacta1)
        horast = profiles.horas_trabajadas
        horast += horas_trabajadas2
    
    profiles.horas_trabajadas = horast  # Actualizar las horas trabajadas en el perfil
    profiles.save()  # Guardar el perfil actualizado
    return redirect('login')  # Redirigir a la página de inicio de sesión

#CARGA MASIVA
@login_required
def carga_masiva(request):
    profiles = Profile.objects.get(user_id = request.user.id)
    if profiles.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    template_name = 'administrator/carga_masiva.html' #administrado/administrador_carga_masiva
    return render(request,template_name,{'template_name':template_name,'profiles':profiles})

@login_required
#se descarga el archivo el archivo
def import_administrator(request):
    profiles = Profile.objects.get(user_id = request.user.id)
    if profiles.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    response = HttpResponse(content_type='application/ms-excel') #bajo un archivo
    response['Content-Disposition'] = 'attachment; filename="archivo_carga_masiva.xls"' #  va a tomar un nombre en particular// carga masiva
    wb = xlwt.Workbook(encoding='utf-8') #creo el libro
    ws = wb.add_sheet('carga_masiva') #creo la hoja con nombre carga_masiva
    row_num = 0
    columns = ['Username','first_name','Last_name','email']#username, first_name, last_name, email
    #----Estilo----
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    #----Estilo----   

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)# primera iteracion Se escribre la filas, 0, nombre habilidad, colocael estilo
                                                                                        #segunda iteracion, 0, nombre habilidad, nivel coloca el estilo
    font_style = xlwt.XFStyle()
    date_format = xlwt.XFStyle()
    date_format.num_format_str = 'dd/MM/yyyy'
    for row in range(1):
        row_num += 1 #una fila más aya
        for col_num in range(4):
            if col_num == 0:
                #se escriben los datos
                ws.write(row_num, col_num, '111.111.111-2' , font_style)
            if col_num == 1:                           
                ws.write(row_num, col_num, 'alannnn' , font_style)
            if col_num == 2:
                ws.write(row_num, col_num, 'alwewe' , font_style)
            if col_num == 3:                           
                ws.write(row_num, col_num, 'alaaaaan@gmail.com' , font_style)
    wb.save(response)
    return response  

@login_required
def carga_masiva_save(request):
    profiles = Profile.objects.get(user_id=request.user.id)
    if profiles.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una área para la que no tiene permisos')
        return redirect('check_group_main')

    if request.method == 'POST':
        if 'myfile' not in request.FILES:
            messages.add_message(request, messages.INFO, 'No se ha enviado ningún archivo')
            return redirect('carga_masiva')
        
        file = request.FILES['myfile']
        try:
            data = pd.read_excel(file)
        except Exception as e:
            messages.add_message(request, messages.INFO, 'Error al leer el archivo Excel: ' + str(e))
            return redirect('carga_masiva')
        acc = 0
        for item in data.itertuples():
            username = str(item[1])
            first_name = str(item[2])
            last_name = str(item[3])
            email = str(item[4])
            rut_exist = User.objects.filter(username=username).count()
            
            if rut_exist == 0:
                user_save = User.objects.create(
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=email
                )
                profile_save = Profile.objects.create(
                    user=user_save,
                    group_id=1,
                    first_session='No',
                    token_app_session='No'
                )
                acc += 1
            
            
    
    
            

        messages.add_message(request, messages.INFO, 'Carga masiva finalizada, se importaron ' + str(acc) + ' registros')
        return redirect('carga_masiva')
@login_required
def admin_dashboard(request):
    #datos tarjeta 1
    usuarios_count = User.objects.all().count()
    #fin datos tarjeta 1
    #datos tarjeta 2
    usuarios_baneados_count = User.objects.filter(is_active='f').all().count()
    #fin datos tarjeta 2
    #tasa de rotación por despido
    tasa_rotacion_despido = round(usuarios_baneados_count / usuarios_count,2)
    #fin datos tarjeta 3
    #datos grafico 1
    #este gráfico nos trae la información de 3 niveles estáticos
    usuarios_total = usuarios_count
    cargo_admin_count = Profile.objects.filter(group_id=1).count()
    cargo_inv_count = Profile.objects.filter(group_id=2).count()
    cargo_ventas_count = Profile.objects.filter(group_id=3).count()
    suma_cargos = cargo_admin_count + cargo_inv_count + cargo_ventas_count
    data_rate = round(float((suma_cargos/usuarios_total)*100),1)
    data_set = [cargo_admin_count,cargo_inv_count,cargo_ventas_count]
    data_label = ['Admin','Inv','Venta']
    data_color = ['#338AFF','#FA1A3C','#28B463']
    #fin datos grafico 1    
    #datos grafico 2    
    #este gráfico nos trae la información de todos los niveles
    cargos_list = Profile.objects.all()#carga una array con todas las habilidades
    data_set_todos_los_cargos = []
    data_label_todos_los_cargos = []
    data_label_todos_los_cargos.append('Total')#agregamos estaticamente la etiqueta total para el gráfico
    data_set_todos_los_cargos.append(usuarios_total)#agregamos el total para que aparezca en el gráfico
    for i in cargos_list:
        data_label_todos_los_cargos.append('Empleado'+str(i.group_id))
        data_set_todos_los_cargos.append(i.group_id) 
    #fin datos grafico 2  
    template_name = 'administrator/admin_dashboard.html'
    return render(request,template_name,{'usuarios_count':usuarios_count,'usuarios_baneados_count':usuarios_baneados_count,'rate_heroes_habilidad':tasa_rotacion_despido,'data_rate':data_rate,'data_set':data_set,'data_label':data_label,'data_color':data_color,'data_set_todos_los_cargos':data_set_todos_los_cargos,'data_label_todos_los_cargos':data_label_todos_los_cargos})
