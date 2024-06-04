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
        producto_array = Producto.objects.filter(producto_state ='Activa').order_by('stock_producto')
        
        for iv in producto_array:
            categoria_data = Category.objects.get(producto_id=iv.id)
            categoria_group = categoria_data.category_group
            
            #se guarda la información del usuario
            producto_all.append({'id':iv.id,'nombre_producto':iv.nombre_producto,'precio_producto':iv.precio_producto,'stock_producto':iv.stock_producto, 'stock_minimo_producto':iv.stock_minimo_producto,'stock_maximo_producto':iv.stock_maximo_producto,'descripcion_producto':iv.descripcion_producto,'categoria_data':categoria_group})
            
    else:#si la cadena de búsqueda trae datos
        #h_count = User.objects.filter(is_active='t').filter(nombre__icontains=search).count()
        #Lógica de busqueda por primer nombre, nombre de usuario, los filtra si están activos o no y se ordena por primer nombre de forma ascendente
        producto_array =  Producto.objects.filter(Q(nombre_producto__icontains=search)).filter(producto_state ='Activa').order_by('-stock_producto')#Ascendente
        for iv in producto_array:
            categoria_data = Category.objects.get(producto_id=iv.id)
            categoria_group = categoria_data.category_group
            #profile = categoria_data.group
            #se guarda la información del usuario
            producto_all.append({'id':iv.id,'nombre_producto':iv.nombre_producto,'precio_producto':iv.precio_producto,'stock_producto':iv.stock_producto, 'stock_minimo_producto':iv.stock_minimo_producto,'stock_maximo_producto':iv.stock_maximo_producto,'descripcion_producto':iv.descripcion_producto,'categoria_data':categoria_group})          
    
    #user_array = User.objects.filter(is_active='t').order_by('first_name')
    #categoria_data = Profile.objects.all()
    paginator = Paginator(producto_all, 30)  
    
    producto_list = paginator.get_page(page)
    print(producto_list)
    template_name = 'inventario/inventario_listado.html'
    return render(request,template_name,{'profiles':profiles,'producto_list':producto_list,'paginator':paginator,'page':page,'search':search })




@login_required
def producto_create(request):
    profiles = Profile.objects.get(user_id = request.user.id)
    if profiles.group_id != 1 and profiles.group_id != 2:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    template_name = 'inventario/producto_create.html'
    category_group_data = Category_group.objects.all()
    return render(request,template_name,{'category_groups':category_group_data})

@login_required
def producto_create3(request,producto_id):
    profiles = Profile.objects.get(user_id = request.user.id)
    if profiles.group_id != 1 and profiles.group_id != 2:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    if request.method == 'POST':
        category_group_id = request.POST.get('category_group_id')
        nombre_producto = request.POST.get('nombre')
        precio_producto = request.POST.get('precio')
        stock_producto = request.POST.get('stock')
        stock_minimo_producto = request.POST.get('stock_minimo')
        stock_maximo_producto = request.POST.get('stock_maximo')
        descripcion_producto = request.POST.get('descripcion_producto')
        producto_data_count = Producto.objects.filter(pk=producto_id).count()
        producto_data = Producto.objects.get(pk=producto_id)

    producto_data = Producto.objects.get(pk=producto_id)
    print("nomre: "+producto_data.nombre_producto)
    category_data = Category.objects.get(producto_id=producto_id)
    category_datas = Category_group.objects.get(pk=category_data.category_group_id) 
    category_groups = Category_group.objects.all().exclude(pk=0).order_by('category_group_name')    
    template_name = 'inventario/producto_create3.html'
    return render(request,template_name,{'producto_data':producto_data,'category_data':category_data,'category_datas':category_datas,'category_groups':category_groups})
    


@login_required
def producto_save(request):
    profiles = Profile.objects.get(user_id = request.user.id)
    if profiles.group_id != 1 and profiles.group_id != 2:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    if request.method == 'POST':
        category_group_id = request.POST.get('category_group_id')
        nombre_producto = request.POST.get('nombre')
        precio_producto = request.POST.get('precio')
        stock_producto = request.POST.get('stock')
        stock_minimo_producto = request.POST.get('stock_minimo')
        stock_maximo_producto = request.POST.get('stock_maximo')
        descripcion_producto = request.POST.get('descripcion_producto')
        validar=True
        Produc_exist = Producto.objects.filter(nombre_producto=nombre_producto).count()

        if Produc_exist == 1:
            validar = False
            messages.add_message(request, messages.INFO, 'Este producto ya a sido creado anteriormente')
            
        if validacion.validar_soloString(nombre_producto) ==False:
            messages.add_message(request, messages.INFO, 'El nombre del producto no puede estar vacio')
            validar=False
        if validacion.validar_int(precio_producto) ==False:
            messages.add_message(request, messages.INFO, 'El precio del producto no puede ser negativo ni nulo')
            validar=False
        if validacion.validar_int(stock_producto) ==False:
            messages.add_message(request, messages.INFO, 'El stock del producto no puede ser negativo ni nulo (si el stock es 0, entonces digitelo)')
            validar=False
        if validacion.validar_int(stock_minimo_producto) ==False:
            messages.add_message(request, messages.INFO, 'El stock minimo del producto no puede ser negativo')
            validar=False    
        if validacion.validar_int(stock_maximo_producto) ==False:
            messages.add_message(request, messages.INFO, 'El stock maximo del producto no puede ser negativo')
            validar=False   
        if stock_minimo_producto > stock_maximo_producto:
            messages.add_message(request, messages.INFO, 'El stock minimo no puede ser maxor al stock maximo del producto')
            validar=False
        if validar == True:
            producto = Producto(
                nombre_producto = nombre_producto,
                precio_producto = precio_producto,
                stock_producto = stock_producto,
                stock_minimo_producto = stock_minimo_producto,
                stock_maximo_producto = stock_maximo_producto,
                descripcion_producto = descripcion_producto,
                )
            producto.save()
            category_save = Category(
                producto_id = producto.id,
                category_group_id = category_group_id,
                
            )
            category_save.save()
            messages.add_message(request, messages.INFO, 'Producto creado con exito')                                                
    template_name = 'inventario/inventario_main.html'
    return render(request,template_name)



@login_required
def producto_edit(request,producto_id):
    profiles = Profile.objects.get(user_id = request.user.id)
    if profiles.group_id != 1 and profiles.group_id != 2:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    if request.method == 'POST':
        category_group_id = request.POST.get('category_group_id')
        nombre_producto = request.POST.get('nombre')
        precio_producto = request.POST.get('precio')
        stock_producto = request.POST.get('stock')
        stock_minimo_producto = request.POST.get('stock_minimo')
        stock_maximo_producto = request.POST.get('stock_maximo')
        
        descripcion_producto = request.POST.get('descripcion_producto')
        producto_data_count = Producto.objects.filter(pk=producto_id).count()
        producto_data = Producto.objects.get(pk=producto_id)
        validar =True
    
        if producto_data.nombre_producto != nombre_producto:
                Produc_exist = Producto.objects.filter(nombre_producto=nombre_producto).count()
                if Produc_exist > 0:
                    #que es page
                    messages.add_message(request, messages.INFO, 'El correo '+str(nombre_producto)+' ya existe en nuestros registros asociado a otro usuario, por favor utilice otro ')
                    validar=False
        if validacion.validar_soloString(nombre_producto)==False:
            messages.add_message(request, messages.INFO, 'El nombre del producto no puede ser nulo')
            validar=False
        if validacion.validar_int(precio_producto) == False:
            messages.add_message(request, messages.INFO, 'El precio del producto no puede ser negativo ni nulo')
            validar=False
        if validacion.validar_int(stock_producto) == False:
            messages.add_message(request, messages.INFO, 'El stock del producto no puede ser negativo')
            validar=False
        if validacion.validar_int(stock_minimo_producto) == False:
            messages.add_message(request, messages.INFO, 'El stock minimo del producto no puede ser negativo')
            validar=False    
        if validacion.validar_int(stock_maximo_producto) == False:
            messages.add_message(request, messages.INFO, 'El stock maximo del producto no puede ser negativo')
            validar=False   
        if int(stock_minimo_producto) > int(stock_maximo_producto):
            messages.add_message(request, messages.INFO, 'El stock minimo no puede ser mayor al stock maximo del producto')
            validar=False
        if validar == True:
            Producto.objects.filter(pk = producto_id).update(nombre_producto = nombre_producto)
            Producto.objects.filter(pk = producto_id).update(precio_producto = precio_producto)  
            Producto.objects.filter(pk = producto_id).update(stock_producto = stock_producto)  
            Category.objects.filter(producto_id = producto_id).update(category_group_id = category_group_id)    
            Producto.objects.filter(pk = producto_id).update(stock_minimo_producto = stock_minimo_producto)
            Producto.objects.filter(pk = producto_id).update(stock_maximo_producto = stock_maximo_producto)  
            Producto.objects.filter(pk = producto_id).update(descripcion_producto = descripcion_producto)  
            messages.add_message(request, messages.INFO, 'Producto  '+producto_data.nombre_producto +' editado con éxito')                             
            return redirect('inventario_listado')
        else:
            messages.add_message(request, messages.INFO, 'Hubo un error al editar el Producto: '+producto_data.nombre_producto )
            return redirect('inventario_listado')    
    producto_data = Producto.objects.get(pk=producto_id)
    category_data = Category.objects.get(producto_id=producto_id)
    category_datas = Category_group.objects.get(pk=category_data.category_group_id) 
    category_groups = Category_group.objects.all().exclude(pk=0).order_by('category_group_name')    
    template_name = 'inventario/producto_edit.html'
    return render(request,template_name,{'producto_data':producto_data,'category_data':category_data,'category_datas':category_datas,'category_groups':category_groups})

@login_required
def producto_ver(request, producto_id):
    profiles = Profile.objects.get(user_id=request.user.id)
    if profiles.group_id != 1 and profiles.group_id != 2:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    producto_data = Producto.objects.get(pk=producto_id)
    category_data = Category.objects.get(producto_id=producto_id)
    category_datas = Category_group.objects.get(pk=category_data.category_group_id) 
    category_groups = Category_group.objects.all().exclude(pk=0).order_by('category_group_name')    
    template_name = 'inventario/producto_ver.html'
    return render(request,template_name,{'producto_data':producto_data,'category_data':category_data,'category_datas':category_datas,'category_groups':category_groups})




@login_required
def producto_delete(request,producto_id):
    profiles = Profile.objects.get(user_id = request.user.id)
    if profiles.group_id != 1 and profiles.group_id !=2:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')

    producto_data_count = Producto.objects.filter(pk=producto_id).count()
    producto_data = Producto.objects.get(pk=producto_id)
    category_data = Category.objects.get(producto_id=producto_id)       
    if producto_data_count == 1:
        #Profile.objects.filter(user_id=user_id).delete()
        Category.objects.filter(producto_id=producto_id).delete()
        Producto.objects.filter(pk=producto_id).delete()
        messages.add_message(request, messages.INFO, 'Producto '+producto_data.nombre_producto +' eliminado con éxito')
        return redirect('inventario_listado')        
    else:
        messages.add_message(request, messages.INFO, 'Hubo un error al eliminar el producto '+producto_data.nombre_producto)
        return redirect('inventario_listado')  
    

@login_required    
def inventario_listado_deactivate(request,page=None,search=None):
    
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
        producto_array = Producto.objects.filter(producto_state ='Deactivate').order_by('stock_producto')
        
        for iv in producto_array:
            categoria_data = Category.objects.get(producto_id=iv.id)
            categoria_group = categoria_data.category_group
            
            #se guarda la información del usuario
            producto_all.append({'id':iv.id,'nombre_producto':iv.nombre_producto,'precio_producto':iv.precio_producto,'stock_producto':iv.stock_producto, 'stock_minimo_producto':iv.stock_minimo_producto,'stock_maximo_producto':iv.stock_maximo_producto,'descripcion_producto':iv.descripcion_producto,'categoria_data':categoria_group})
            
    else:#si la cadena de búsqueda trae datos
        #h_count = User.objects.filter(is_active='t').filter(nombre__icontains=search).count()
        #Lógica de busqueda por primer nombre, nombre de usuario, los filtra si están activos o no y se ordena por primer nombre de forma ascendente
        producto_array =  Producto.objects.filter(Q(nombre_producto__icontains=search)).filter(producto_state ='Deactivate').order_by('-stock_producto')#Ascendente
        for iv in producto_array:
            categoria_data = Category.objects.get(producto_id=iv.id)
            categoria_group = categoria_data.category_group
            #profile = categoria_data.group
            #se guarda la información del usuario
            producto_all.append({'id':iv.id,'nombre_producto':iv.nombre_producto,'precio_producto':iv.precio_producto,'stock_producto':iv.stock_producto, 'stock_minimo_producto':iv.stock_minimo_producto,'stock_maximo_producto':iv.stock_maximo_producto,'descripcion_producto':iv.descripcion_producto,'categoria_data':categoria_group})          
    
    #user_array = User.objects.filter(is_active='t').order_by('first_name')
    #categoria_data = Profile.objects.all()
    paginator = Paginator(producto_all, 2)  
    
    producto_list = paginator.get_page(page)
    print(producto_list)
    template_name = 'inventario/inventario_listado_deactivate.html'
    return render(request,template_name,{'profiles':profiles,'producto_list':producto_list,'paginator':paginator,'page':page,'search':search })


@login_required
def producto_deactivate(request,producto_id):
    profiles = Profile.objects.get(user_id = request.user.id)
    if profiles.group_id != 1 and profiles.group_id !=2:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')

    producto_data_count = Producto.objects.filter(pk=producto_id).count()
    producto_data = Producto.objects.get(pk=producto_id)       
    if producto_data_count == 1:
        Producto.objects.filter(pk=producto_id).update(producto_state='Deactivate')
        messages.add_message(request, messages.INFO, 'Producto '+producto_data.nombre_producto +' desactivado con éxito')
        return redirect('inventario_listado')        
    else:
        messages.add_message(request, messages.INFO, 'Hubo un error al desactivar el producto '+producto_data.nombre_producto)
        return redirect('inventario_listado')  
@login_required
def producto_activate(request,producto_id):
    profiles = Profile.objects.get(user_id = request.user.id)
    if profiles.group_id != 1 and profiles.group_id !=2:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')

    producto_data_count = Producto.objects.filter(pk=producto_id).count()
    producto_data = Producto.objects.get(pk=producto_id)       
    if producto_data_count == 1:
        Producto.objects.filter(pk=producto_id).update(producto_state='Activa')
        messages.add_message(request, messages.INFO, 'Producto '+producto_data.nombre_producto +' Activado con éxito')
        return redirect('inventario_listado_deactivate')        
    else:
        messages.add_message(request, messages.INFO, 'Hubo un error al activar el producto '+producto_data.nombre_producto)
        return redirect('inventario_listado_deactivate') 


@login_required
def categories_create(request):
    profiles = Profile.objects.get(user_id = request.user.id)
    if profiles.group_id != 1 and profiles.group_id != 2:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    template_name = 'inventario/categories_create.html'
    return render(request,template_name)

@login_required
def categories_save(request):

    
    if request.method=='POST':
        name= request.POST.get('name')
        state=True
        validar = True
        categories_exist = Category.objects.filter(category_group_name=name).count()
        if categories_exist==1:
            validar=False
            messages.add_message(request,messages.INFO,'Solo puede haber un tipo de categoria')
        if validacion.validar_soloString(name)==False:
            validar=False
            messages.add_message(request,messages.INFO,'El nombre solo debe contener letras, y el campo no debe estar vacio')
        
        if validar==True:
            categories_save=Category_group(
                category_group_name=name.capitalize(),
            )
            
            categories_save.save()
    messages.add_message(request,messages.INFO,'Categoria creada con exito')
    return redirect('inventario_main')


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
#CARGA MASIVA
@login_required
def carga_masiva2(request):
    profiles = Profile.objects.get(user_id = request.user.id)
    if profiles.group_id != 1 and profiles.group_id != 2:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    template_name = 'inventario/carga_masiva2.html' #administrado/administrador_carga_masiva
    return render(request,template_name,{'template_name':template_name,'profiles':profiles})

@login_required
#se descarga el archivo el archivo
def import_inventario(request):
    profiles = Profile.objects.get(user_id = request.user.id)
    if profiles.group_id != 1 and profiles.group_id != 2:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    response = HttpResponse(content_type='application/ms-excel') #bajo un archivo
    response['Content-Disposition'] = 'attachment; filename="archivo_carga_masiva_inventario.xls"' #  va a tomar un nombre en particular// carga masiva
    wb = xlwt.Workbook(encoding='utf-8') #creo el libro
    ws = wb.add_sheet('carga_masiva') #creo la hoja con nombre carga_masiva
    row_num = 0
    columns = ['nombre_producto','precio_producto','stock_producto','descripcion_producto','estado_producto']#username, first_name, last_name, email
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
        for col_num in range(5):
            if col_num == 0:
                #se escriben los datos
                ws.write(row_num, col_num, 'Procesador' , font_style)
            if col_num == 1:                           
                ws.write(row_num, col_num, '125000' , font_style)
            if col_num == 2:
                ws.write(row_num, col_num, '10' , font_style)
            if col_num == 3:                           
                ws.write(row_num, col_num, 'nucleo' , font_style)
            if col_num == 4:                           
                ws.write(row_num, col_num, 'bajo' , font_style)
    wb.save(response)
    return response  

@login_required
def carga_masiva_save2(request):
    profiles = Profile.objects.get(user_id=request.user.id)
    if profiles.group_id != 1 and profiles.group_id != 2:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una área para la que no tiene permisos')
        return redirect('check_group_main')

    if request.method == 'POST':
        if 'myfile' not in request.FILES:
            messages.add_message(request, messages.INFO, 'No se ha enviado ningún archivo')
            return redirect('carga_masiva2')
        
        file = request.FILES['myfile']
        try:
            data = pd.read_excel(file)
        except Exception as e:
            messages.add_message(request, messages.INFO, 'Error al leer el archivo Excel: ' + str(e))
            return redirect('carga_masiva2')

        acc = 0
        for item in data.itertuples():
            nombre_producto = str(item[1])
            precio_producto = int(item[2])
            stock_producto = int(item[3])
            descripcion_producto = str(item[4])
            estado_producto = str(item[5])

            inventario_save = Producto(
                nombre_producto=nombre_producto,
                precio_producto=precio_producto,
                stock_producto=stock_producto,
                descripcion_producto=descripcion_producto,
                estado_producto=estado_producto,
            )
            inventario_save.save()
            category_save = Category(
                producto_id = inventario_save.id,
            )
            category_save.save()
            

            acc += 1

        messages.add_message(request, messages.INFO, 'Carga masiva finalizada, se importaron ' + str(acc) + ' registros')
        return redirect('carga_masiva2')
    
    
def inventario_dashboard(request):
    #datos tarjeta 1
    productos_count = Producto.objects.all().count()
    #fin datos tarjeta 1
    #datos tarjeta 2
    categorias_productos = Category_group.objects.all().count()
    #fin datos tarjeta 2
    #tasa de rotación por despido
    tasa_producto_grupo = round(categorias_productos / productos_count,2)
    #fin datos tarjeta 3
    #datos grafico 1
    #este gráfico nos trae la información de 3 niveles estáticos
    usuarios_total = productos_count
    no_grupo_count = Category_group.objects.filter(id=0).count()
    tarjetas_count = Category_group.objects.filter(id=2).count()
    procesadores_count = Category_group.objects.filter(id=3).count()
    suma_cargos = no_grupo_count + tarjetas_count + procesadores_count
    data_rate = round(float((suma_cargos/usuarios_total)*100),1)
    data_set = [no_grupo_count,tarjetas_count,procesadores_count]
    data_label = ['Sin Grupo','Graficas','Procesadores']
    data_color = ['#338AFF','#FA1A3C','#28B463']
    #fin datos grafico 1    
    #datos grafico 2    
    #este gráfico nos trae la información de todos los niveles
    cargos_list = Category_group.objects.all()#carga una array con todas las habilidades
    data_set_todos_los_cargos = []
    data_label_todos_los_cargos = []
    data_label_todos_los_cargos.append('Total')#agregamos estaticamente la etiqueta total para el gráfico
    data_set_todos_los_cargos.append(usuarios_total)#agregamos el total para que aparezca en el gráfico
    for i in cargos_list:
        data_label_todos_los_cargos.append('Grupo'+str(i.id))
        data_set_todos_los_cargos.append(i.id) 
    #fin datos grafico 2  
    template_name = 'inventario/inventario_dashboard.html'
    return render(request,template_name,{'productos_count':productos_count,'categorias_productos':categorias_productos,'rate_heroes_habilidad':tasa_producto_grupo,'data_rate':data_rate,'data_set':data_set,'data_label':data_label,'data_color':data_color,'data_set_todos_los_cargos':data_set_todos_los_cargos,'data_label_todos_los_cargos':data_label_todos_los_cargos})


# Create your views here.
@login_required
def categories_create(request):
    profiles = Profile.objects.get(user_id = request.user.id)
    if profiles.group_id != 1 and profiles.group_id != 2:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    template_name = 'inventario/categories_create.html'
    return render(request,template_name)

@login_required
def categories_save(request):

    if request.method=='POST':
        name= request.POST.get('name')
        state=True
        validar = True
        categories_exist = Category_group.objects.filter(category_group_name=name).count()
        if categories_exist==1:
            validar=False
            messages.add_message(request,messages.INFO,'Solo puede haber un tipo de categoria')
        if validacion.validar_soloString(name)==False:
            validar=False
            messages.add_message(request,messages.INFO,'El nombre no debe contener solo numeros y no debe estar vacio')
        
        if validar==True:
            categories_save=Category_group(
                category_group_name=name,
            )
            
            categories_save.save()
            messages.add_message(request,messages.INFO,'Categoria creada con exito')
    return redirect('inventario_main')
    

@login_required
def categories_delete(request,categories_id):
    profiles = Profile.objects.get(user_id = request.user.id)
    if profiles.group_id != 1 and profiles.group_id != 2:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')

    category_data_count = Category_group.objects.filter(pk=categories_id).count()
    category_data = Category_group.objects.get(pk=categories_id)     
    if category_data_count == 1:
        
        categoria = Category.objects.filter(category_group_id=categories_id)
        for c in categoria:
            id_producto = c.producto_id
            Producto.objects.get(pk = id_producto).delete()
            
        
        Category.objects.filter(category_group_id=categories_id).delete()
        Category_group.objects.get(pk=categories_id).delete()
        messages.add_message(request, messages.INFO, 'Categoria '+category_data.category_group_name +' eliminada con éxito')
        return redirect('list_categories_active')        
    else:
        messages.add_message(request, messages.INFO, 'Hubo un error al eliminar la Categoria '+category_data.category_group_name)
        return redirect('categories_listado')

    
@login_required    
def list_categories(request,page=None,search=None):
    
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
    print("search> ",search)
    categories_all = [] #lista vacia para agrega la salida de la lista ya sea con la cadena de búsqueda o no
    if search == None or search == "None":# si la cadena de búsqueda viene vacia
        #categories_all=Category_group.objects.all()
        categories_all = Category_group.objects.filter(category_state='Activa')#.order_by('category_group')
        paginator = Paginator(categories_all, 1)  
        categories_list = paginator.get_page(page)
        template_name = 'inventario/list_categories.html'
        return render(request,template_name,{'profiles':profiles,'categories_list':categories_list,'paginator':paginator,'page':page,'search':search })
    else:#si la cadena de búsqueda trae datos
        categories_all =  Category_group.objects.filter(category_group_name=search).filter(category_state='Activa').order_by('category_group_name')#Ascendente         
        paginator = Paginator(categories_all, 1)  
        categories_list = paginator.get_page(page)
        template_name = 'inventario/list_categories.html'
        return render(request,template_name,{'profiles':profiles,'categories_list':categories_list,'paginator':paginator,'page':page,'search':search })
@login_required
def categories_deactivate(request,categories_id):
    profiles= Profile.objects.get(user_id = request.user.id)
    if profiles.group_id != 1 and profiles.group_id != 2:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    new_state = 'Deactivate'
    category_data_count = Category_group.objects.filter(pk=categories_id).count()
    category_data = Category_group.objects.get(pk=categories_id) 
    categoria = Category.objects.filter(category_group_id=categories_id)
    if category_data_count == 1:
        for c in categoria:
            id_producto = c.producto_id
            Producto.objects.filter(pk = id_producto).update(producto_state='Deactivate')
        Category_group.objects.filter(pk = categories_id).update(category_state = new_state)
        messages.add_message(request, messages.INFO, 'Categoria  '+ category_data.category_group_name +' desactivada con éxito')                             
        return redirect('list_categories_active')
    else:
        messages.add_message(request, messages.INFO, 'Hubo un error al desactivar la categoria: '+category_data.category_group_name )
        return redirect('list_categories_active') 
@login_required
def categories_activate(request,categories_id):
    profiles= Profile.objects.get(user_id = request.user.id)
    if profiles.group_id != 1 and profiles.group_id != 2:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    new_state = 'Activa'
    category_data_count = Category_group.objects.filter(pk=categories_id).count()
    category_data = Category_group.objects.get(pk=categories_id) 
    categoria = Category.objects.filter(category_group_id=categories_id)
    if category_data_count == 1:
        for c in categoria:
            id_producto = c.producto_id
            Producto.objects.filter(pk = id_producto).update(producto_state='Activa')
        Category_group.objects.filter(pk = categories_id).update(category_state = new_state)
        messages.add_message(request, messages.INFO, 'Categoria  '+ category_data.category_group_name +' activada con éxito')                             
        return redirect('list_categories_deactivate')
    else:
        messages.add_message(request, messages.INFO, 'Hubo un error al desactivar la categoria: '+category_data.category_group_name )
        return redirect('list_categories_deactivate') 

def categories_edit(request,categories_id):
    profiles = Profile.objects.get(user_id = request.user.id)
    if profiles.group_id != 1 and profiles.group_id != 2:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    if request.method == 'POST':
        category_group_name = request.POST.get('nombre')
        if validacion.validar_soloString(category_group_name)==False:
            messages.add_message(request,messages.INFO,'El nombre de la categoria no debe estar vacio y no debe contener solo numeros')
        category_data_count = Category_group.objects.filter(pk=categories_id).count()
        category_data = Category_group.objects.get(pk=categories_id) 
        if category_data_count == 1:

            Category_group.objects.filter(pk = categories_id).update(category_group_name = category_group_name)
            messages.add_message(request, messages.INFO, 'Categoria  '+ category_data.category_group_name +' editado con éxito')                             
            return redirect('list_categories_active')
        else:
            messages.add_message(request, messages.INFO, 'Hubo un error al editar la categoria: '+category_data.category_group_name )
            return redirect('list_categories_active')    
        
    category_data = Category_group.objects.get(pk=categories_id) 
    
    template_name = 'inventario/categories_edit.html'
    return render(request,template_name,{'category_data':category_data})



"""@login_required
def categories_save_edit(request, categories_id):

    if request.method=='POST':
        name= request.POST.get('name')
        state=True
        if name=='':
            messages.add_message(request,messages.INFO,'Debe ingresar un nombre para la categoria')
            return('categories_create')    
        categories_save=Category_group(
            category_group_name=name,
        )
    category_group_name.filter(pk=categories_id).update(name=name)
    messages.add_message(request,messages.INFO,'Categoria actualizada con exito')
    return redirect('inventario_main')"""

def categories_save_edit(request, categories_id):
    profiles = Profile.objects.get(user_id=request.user.id)
    if profiles.group_id != 1 and profiles.group_id != 2:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    template_name = 'inventario/categories_edit.html' 
    name = request.POST.get('name')
    Category_group.objects.filter(pk=categories_id).update(category_group_name=name)
    return render(request, template_name, {'template_name': template_name, 'profiles': profiles, 'categories_id': categories_id})

def categories_ver(request, categories_id):
    profiles = Profile.objects.get(user_id=request.user.id)
    if profiles.group_id != 1 and profiles.group_id != 2:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    template_name = 'inventario/categories_ver.html' 
    Category_group.objects.filter(pk=categories_id)
    category_data = Category_group.objects.get(pk=categories_id) 
    return render(request, template_name, {'template_name': template_name, 'profiles': profiles, 'categories_id': categories_id,'category_data':category_data})

@login_required    
def list_categories_deactivate(request,page=None,search=None):
    
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
    print("search> ",search)
    categories_all = [] #lista vacia para agrega la salida de la lista ya sea con la cadena de búsqueda o no
    if search == None or search == "None":# si la cadena de búsqueda viene vacia
        #categories_all=Category_group.objects.all()
        categories_all = Category_group.objects.filter(category_state='Deactivate')#.order_by('category_group')
        paginator = Paginator(categories_all, 1)  
        categories_list = paginator.get_page(page)
        template_name = 'inventario/list_categories_deactivate.html'
        return render(request,template_name,{'profiles':profiles,'categories_list':categories_list,'paginator':paginator,'page':page,'search':search })
    else:#si la cadena de búsqueda trae datos
        categories_all =  Category_group.objects.filter(category_group_name=search).order_by('category_group_name')#Ascendente         
        paginator = Paginator(categories_all, 1)  
        categories_list = paginator.get_page(page)
        template_name = 'inventario/list_categories_deactivate.html'
        return render(request,template_name,{'profiles':profiles,'categories_list':categories_list,'paginator':paginator,'page':page,'search':search })
    