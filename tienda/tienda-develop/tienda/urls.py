from django.urls import path
from . import views


urlpatterns = [
    path('', views.productos),
    path('carrito/', views.carrito),
    path('pedido/', views.pedido),
    path('pedido/creado/', views.ver_pedido),
]
