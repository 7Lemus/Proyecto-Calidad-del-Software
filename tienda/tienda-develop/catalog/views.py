from django.shortcuts import redirect, render
from .forms import Pago
from .models import Producto
import json


def index(request):
    context = {
        'products': Producto.objects.all()
    }
    return render(request, 'catalog/index.html', context)


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
    return render(request, 'catalog/carrito.html', { 'carrito': carrito })


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
    return render(request, 'catalog/pedido.html', context)


def ver_pedido(request):
    return render(request, 'catalog/ver_pedido.html', {})
