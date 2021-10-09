from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from .forms import UserForm, UpdateUserForm
from tienda.models import Producto, Usuario


@login_required(login_url='/acceder/')
def inventario(request):
    if request.user.tipo not in ('A', 'E'):
        messages.error(request, 'Acceso sólo para empleados y administradores.', extra_tags='danger')
        return redirect('/perfil/')
    p = Producto.objects.all()
    context = {
        'section': 'inventario',
        'productos': p,
    }
    return render(request, 'administracion/inventario.html', context)


@login_required(login_url='/acceder/')
def nuevo_usuario(request):
    if request.user.tipo != 'A':
        messages.error(request, 'Acceso sólo para administradores.', extra_tags='danger')
        return redirect('/perfil/')
    form = UserForm()
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('first_name')
            messages.success(request, 'Usuario %s registrado exitosamente.' % name)
            form.save()
            return redirect('/administracion/usuarios/')
    context = {
        'section': 'usuarios.nuevo',
        'form': form,
        'estados': {
            'C': 'Cliente',
            'E': 'Empleado',
            'A': 'Administrador',
        }
    }
    return render(request, 'administracion/usuarios.nuevo.html', context)


@login_required(login_url='/acceder/')
def usuarios(request):
    if request.user.tipo != 'A':
        messages.error(request, 'Acceso sólo para administradores.', extra_tags='danger')
        return redirect('/perfil/')
    u = Usuario.objects.filter(id__gt=1)
    context = {
        'section': 'usuarios',
        'usuarios': u,
        'estados': {
            'C': 'Cliente',
            'E': 'Empleado',
            'A': 'Administrador',
        }
    }
    return render(request, 'administracion/usuarios.html', context)
