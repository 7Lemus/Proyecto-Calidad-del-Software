from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import redirect, render
from .forms import UserForm, UpdateUserForm


def index(request):
    context = {
        'carousel': [
            {'id': 0, 'src': '/static/img/oferta2.png', 'alt': 'oferta', 'extra_class': 'active'},
            {'id': 1, 'src': '/static/img/oferta1.png', 'alt': 'oferta', 'extra_class': ''},
            {'id': 2, 'src': '/static/img/oferta2.png', 'alt': 'oferta', 'extra_class': ''}
        ]
    }
    return render(request, 'index.html', context)


def registrar(request):
    if request.user.is_authenticated:
        return redirect('/')
    form = UserForm()
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('first_name')
            messages.success(request, 'Gracias por registrarte %s, intenta acceder a tu cuenta.' % name)
            form.save()
            return redirect('/acceder/')
    context = {"form": form}
    return render(request, 'usuario/registro.html', context)


def acceder(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect(request.GET.get('next') or '/perfil/')
        else:
            messages.error(request, 'Usuario o contraseña inválidos!', extra_tags='danger')
    return render(request, 'usuario/acceso.html', {})


def salir(request):
    logout(request)
    return redirect('/acceder/')


@login_required(login_url='/acceder/')
def perfil(request):
    form = UpdateUserForm()
    if request.method == 'POST':
        form = UpdateUserForm(request.POST)
        if form.is_valid():
            user = request.user
            user.email = form.cleaned_data.get('email')
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            form.save(commit=False)
            user.save()
            messages.success(request, '¡Tu perfil se ha actualizado exitosamente!')
        else:
            messages.error(request, 'Hubo un error al actualizar el perfil.', extra_tags='danger')
    context = {
        'section': 'perfil',
        'form': form
    }
    return render(request, 'usuario/perfil.html', context)


@login_required(login_url='/acceder/')
def contrasena(request):
    form = PasswordChangeForm(request.user)
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, '¡Tu contraseña se ha actualizado exitosamente.')
        else:
            messages.error(request, 'Hubo un error al actualizar contraseña.', extra_tags='danger')
    context = {
        'section': 'contraseña',
        'form': form
    }
    return render(request, 'usuario/perfil.contrasena.html', context)


@login_required(login_url='/acceder/')
def direcciones(request):
    context = {
        'section': 'direcciones',
    }
    return render(request, 'usuario/perfil.direcciones.html', context)


@login_required(login_url='/acceder/')
def pedidos(request):
    context = {
        'section': 'pedidos',
    }
    return render(request, 'usuario/perfil.pedidos.html', context)
