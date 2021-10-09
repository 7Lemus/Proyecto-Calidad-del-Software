from django.urls import path
from . import views


urlpatterns = [
    path('inventario/', views.inventario),
    path('usuarios/', views.usuarios),
    path('usuarios/nuevo/', views.nuevo_usuario),
]
