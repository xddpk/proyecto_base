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
# Create your views here.
#numero de elementos para el listado
global num_elemento 
num_elemento = 1



@login_required
def venta_main(request):
    profiles = Profile.objects.get(user_id = request.user.id)
    if profiles.group_id != 1 and profiles.group_id != 4:
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