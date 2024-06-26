from django.shortcuts import render
from django.conf import settings #importa el archivo settings
from django.contrib import messages #habilita la mesajería entre vistas
from django.contrib.auth.decorators import login_required #habilita el decorador que se niega el acceso a una función si no se esta logeado
from django.contrib.auth.models import Group, User # importa los models de usuarios y grupos
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator #permite la paqinación
from django.db.models import Avg, Count, Q #agrega funcionalidades de agregación a nuestros QuerySets
from django.http import (HttpResponse, HttpResponseBadRequest,
                         HttpResponseNotFound, HttpResponseRedirect) #Salidas alternativas al flujo de la aplicación se explicará mas adelante
from django.shortcuts import redirect, render #permite renderizar vistas basadas en funciones o redireccionar a otras funciones
from django.template import RequestContext # contexto del sistema
from django.views.decorators.csrf import csrf_exempt #decorador que nos permitira realizar conexiones csrf
from registration.models import Profile #importa el modelo profile, el que usaremos para los perfiles de usuarios

# Create your views here.
def home(request):
    return redirect('login')

@login_required
def pre_check_profile(request):
    profile = Profile.objects.filter(user_id=request.user.id).first() # Obtener el perfil del usuario
    if profile: # Si el perfil existe
        if profile.first_session == 'Si': # Si es la primera sesión
            Profile.objects.filter(user_id = request.user.id).update(first_session = 'No')  
            Profile.objects.filter(user_id = request.user.id).update(token_app_session = 'No') 
            return redirect('admin_main') # Redirigir a la página de cambio de contraseña
    
def check_profile(request):
    try:
        profile = Profile.objects.get(user_id=request.user.id)
    except Profile.DoesNotExist:
        messages.add_message(request, messages.INFO, 'No se encontró el perfil asociado a su usuario. Por favor, contacte a los administradores.')
        return redirect('login')
    profile_datos=Profile.objects.get(user_id=request.user.id)
    if (profile.group_id == 1 or profile.group_id == 2 or profile.group_id == 3 or profile.group_id == 4):

        inicio_sesion = profile.first_session
        if inicio_sesion == 'No':
            return redirect('admin_main')
        elif inicio_sesion == 'Si':
            profile.first_session = 'No'
            profile.save()
    
        return render(request, 'registration/password_change_form.html', {'profile_id': Profile.objects.get(user_id=request.user.id).id})


def check_group_main(request):
    return render(request, 'core/check_group_main.html')

