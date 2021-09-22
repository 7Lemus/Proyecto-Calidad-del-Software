from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from .forms import Pago
from .models import Producto
import json


def productos(request):
    context = {
        'products': Producto.objects.all()
    }
    return render(request, 'tienda/productos.html', context)


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
def pedido(request):
    if 'carrito' not in request.COOKIES or request.COOKIES['carrito'] == '{}':
        return redirect('/tienda/carrito/')
    pedido = []
    total = 0
    for k, v in json.loads(request.COOKIES['carrito']).items():
        product = Producto.objects.get(pk=int(k))
        total += product.precio * v['quantity']
        pedido.append({
            'quantity': v['quantity'],
            'subtotal': product.precio * v['quantity'],
            'product': product
        })
    context = { 'pedido': pedido, 'total': total }
    if (request.method == 'POST'):
        pago = Pago(request.POST)
        context['form'] = pago
        if pago.is_valid():
            # TODO almacenar en DB
            return redirect('/tienda/pedido/creado/')
    else:
        context['form'] = Pago()
    return render(request, 'tienda/pedido.html', context)


@login_required(login_url='/acceder/')
def ver_pedido(request):
    return render(request, 'tienda/ver_pedido.html', {})
