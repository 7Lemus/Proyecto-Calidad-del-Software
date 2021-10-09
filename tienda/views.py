from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from .forms import NuevaCompra
from .models import Producto, Direccion, Compra, Detalle
import json


def productos(request):
    context = {
        'products': Producto.objects.all()
    }
    return render(request, 'tienda/productos.html', context)


def producto(request, id):
    p = Producto.objects.filter(id=id)
    if not p:
        return redirect('/tienda/')
    context = {
        'product': p.first()
    }
    return render(request, 'tienda/producto.html', context)


def carrito(request):
    carrito = []
    if 'carrito' in request.COOKIES:
        for k, v in json.loads(request.COOKIES['carrito']).items():
            product = Producto.objects.get(pk=int(k))
            carrito.append({
                'quantity': v['quantity'],
                'subtotal': product.precio * v['quantity'],
                'product': product
            })
    return render(request, 'tienda/carrito.html', { 'carrito': carrito })


@login_required(login_url='/acceder/')
def crear_compra(request):
    if request.user.tipo != 'C':
        messages.error(request, 'Acceso sólo para clientes.', extra_tags='danger')
        return redirect('/perfil/')
    if 'carrito' not in request.COOKIES or request.COOKIES['carrito'] == '{}':
        return redirect('/tienda/carrito/')
    direcciones = Direccion.objects.filter(usuario=request.user)
    if not direcciones:
        messages.error(request, 'Por favor, registre una dirección antes de hacer una compra.', extra_tags='danger')
        return redirect('/perfil/direcciones/registrar/')
    detalle_compra = []
    total = 0
    for k, v in json.loads(request.COOKIES['carrito']).items():
        product = Producto.objects.get(pk=int(k))
        total += product.precio * v['quantity']
        detalle_compra.append({
            'quantity': v['quantity'],
            'subtotal': product.precio * v['quantity'],
            'product': product
        })
    form = NuevaCompra()
    if (request.method == 'POST'):
        form = NuevaCompra(request.POST)
        if form.is_valid():
            c = Compra(
                total = total,
                usuario = request.user,
                nombre = form.cleaned_data.get('nombre'),
                nit = form.cleaned_data.get('nit'),
                direccion = form.cleaned_data.get('direccion'),
                telefono = form.cleaned_data.get('telefono'),
            )
            c.save()  #commit=True
            for detalle in detalle_compra:
                d = Detalle(
                    cantidad = detalle['quantity'],
                    total = detalle['subtotal'],
                    compra = c,
                    producto = detalle['product']
                )
                d.save()
            response = redirect('/tienda/compra/exitosa')
            response.delete_cookie('carrito')
            return response
    context = {
        'detalles': detalle_compra,
        'total': total,
        'form': form,
        'direcciones': direcciones
    }
    return render(request, 'tienda/compra.html', context)


@login_required(login_url='/acceder/')
def compra_exitosa(request):
    if request.user.tipo != 'C':
        messages.error(request, 'Acceso sólo para clientes.', extra_tags='danger')
        return redirect('/perfil/')
    return render(request, 'tienda/compra.exitosa.html', {})
