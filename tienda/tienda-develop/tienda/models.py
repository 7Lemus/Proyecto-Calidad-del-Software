from django.db import models
from django.contrib.auth.models import AbstractUser


class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    estado = models.CharField(max_length=1, choices=[('A', 'Activa'), ('I', 'Inactiva')], default='A')

    def __str__(self):
        return self.nombre


class Fabrica(models.Model):
    nombre = models.CharField(max_length=100)
    estado = models.CharField(max_length=1, choices=[('A', 'Activa'), ('I', 'Inactiva')], default='A')
    tipo = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    unidades = models.IntegerField(default=0)
    moneda = models.CharField(max_length=3, default='Q')
    precio = models.DecimalField(max_digits=5, decimal_places=2)
    precio_compra = models.DecimalField(max_digits=5, decimal_places=2)
    imagen = models.CharField(max_length=255)
    estado = models.CharField(max_length=1, choices=[('A', 'Activa'), ('I', 'Inactiva')], default='A')
    categoria = models.ForeignKey('Categoria', on_delete=models.CASCADE)
    fabrica = models.ForeignKey('Fabrica', on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre


class Pedido(models.Model):
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=6, decimal_places=2)
    estado = models.CharField(max_length=1, choices=[('1', 'Procesando'), ('2', 'En camino'), ('3', 'Entregado')], default='1')
    nit = models.CharField(max_length=12)
    direccion = models.ForeignKey('Direccion', on_delete=models.CASCADE)
    usuario = models.ForeignKey('Usuario', on_delete=models.CASCADE)

    def __str__(self):
        return 'Pedido #' + self.id


class DetallePedido(models.Model):
    cantidad = models.IntegerField()
    total = models.DecimalField(max_digits=5, decimal_places=2)
    pedido = models.ForeignKey('Pedido', on_delete=models.CASCADE)
    producto = models.ForeignKey('Producto', on_delete=models.CASCADE)

    def __str__(self):
        return 'Pedido #' + pedido.id + ' | Detalle #' + self.id


class Compra(models.Model):
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=6, decimal_places=2)
    estado = models.CharField(max_length=1, choices=[('I', 'Ingresada'), ('C', 'Cancelada'), ('E', 'Entregada')], default='I')
    usuario = models.ForeignKey('Usuario', on_delete=models.CASCADE)

    def __str__(self):
        return 'Compra #' + self.id


class DetalleCompra(models.Model):
    cantidad = models.IntegerField()
    total = models.DecimalField(max_digits=5, decimal_places=2)
    compra = models.ForeignKey('Compra', on_delete=models.CASCADE)
    producto = models.ForeignKey('Producto', on_delete=models.CASCADE)

    def __str__(self):
        return 'Compra #' + compra.id + ' | Detalle #' + self.id


class Usuario(AbstractUser):
    email = models.EmailField(unique=True)
    # tipo = models.CharField(max_length=1, choices=[('C', 'Cliente'), ('E', 'Empleado')], default='C')

    def __str__(self):
        return self.first_name + ' ' + self.last_name


class Direccion(models.Model):
    departamento = models.CharField(max_length=50)
    municipio = models.CharField(max_length=50)
    zona = models.IntegerField(default=1)
    direccion = models.CharField(max_length=50)
    referencia = models.TextField()
    usuario = models.ForeignKey('Usuario', on_delete=models.CASCADE)
