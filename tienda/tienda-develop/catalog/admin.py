from django.contrib import admin
from .models import *


admin.site.register(Categoria)
admin.site.register(Producto)
admin.site.register(Fabrica)
admin.site.register(ProductoFabrica)
admin.site.register(Cliente)
admin.site.register(Usuario)
admin.site.register(Pedido)
admin.site.register(PedidoDetalle)
admin.site.register(CargarArticulo)
