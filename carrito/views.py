from django.shortcuts import render

# Create your views here.


def tienda(request):
    template_name = 'carrito/tienda.html'
    return render(request,template_name)


"""
def venta_create(request):
  
    profiles = Profile.objects.get(user_id = request.user.id)
    if profiles.group_id != 1 and profiles.group_id != 4:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    """
    
