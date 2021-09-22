from django.urls import path
from . import views


urlpatterns = [
    path('', views.index),
    path('registrar/', views.registrar),
    path('acceder/', views.acceder),
    path('perfil/', views.perfil),
    path('perfil/contrasena/', views.contrasena),
    path('perfil/direcciones/', views.direcciones),
    path('perfil/pedidos/', views.pedidos),
    path('salir/', views.salir),
]
