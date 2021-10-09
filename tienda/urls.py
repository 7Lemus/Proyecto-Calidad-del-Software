from django.urls import path
from . import views


urlpatterns = [
    path('', views.productos),
    path('producto/<int:id>/', views.producto),
    path('carrito/', views.carrito),
    path('compra/', views.crear_compra),
    path('compra/exitosa', views.compra_exitosa)
]
