from django.db import models


class Categoria(models.Model):
    nombre = models.CharField(max_length=45)
    estado = models.CharField(max_length=45)

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    nombre = models.CharField(max_length=45)
    descripcion = models.TextField()
    estado = models.CharField(max_length=45)
    moneda = models.CharField(max_length=3)
    precio = models.DecimalField(max_digits=5, decimal_places=2)
    categoria = models.ForeignKey("Categoria", on_delete=models.CASCADE)
    imagen = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre


class Fabrica(models.Model):
    nombre = models.CharField(max_length=45)
    estado = models.CharField(max_length=45)
    tipo = models.CharField(max_length=45)

    def __str__(self):
        return self.nombre


class ProductoFabrica(models.Model):
    producto = models.ForeignKey("Producto", on_delete=models.CASCADE)
    fabrica = models.ForeignKey("Fabrica", on_delete=models.CASCADE)
    existencia = models.IntegerField()
    min_existencia = models.IntegerField()
    max_existencia = models.IntegerField()

    def __str__(self):
        return self.producto.nombre + ' - ' + self.fabrica.nombre


class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    tipo = models.CharField(max_length=45)
    direccion = models.CharField(max_length=255)
    estado = models.CharField(max_length=45)
    nit = models.CharField(max_length=12)
    dpi = models.CharField(max_length=16)
    balance = models.DecimalField(max_digits=6, decimal_places=2)
    descuento = models.IntegerField()

    def __str__(self):
        return self.nombre + ' ' + self.apellido


class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    rol = models.CharField(max_length=45)
    direccion = models.CharField(max_length=255)
    estado = models.CharField(max_length=45)
    nit = models.CharField(max_length=12)
    dpi = models.CharField(max_length=16)

    def __str__(self):
        return self.nombre + ' ' + self.apellido


class Pedido(models.Model):
    fecha = models.DateTimeField(auto_now_add=True)
    cantidad = models.IntegerField()
    total = models.DecimalField(max_digits=6, decimal_places=2)
    estado = models.CharField(max_length=45)
    cliente = models.ForeignKey("Cliente", on_delete=models.CASCADE)

    def __str__(self):
        return 'Pedido #' + self.id


class PedidoDetalle(models.Model):
    cantidad = models.IntegerField()
    pedido = models.ForeignKey("Pedido", on_delete=models.CASCADE)
    producto_fabrica = models.ForeignKey("ProductoFabrica", on_delete=models.CASCADE)

    def __str__(self):
        return 'PedidoDetalle #' + self.id


class CargarArticulo(models.Model):
    fecha = models.DateTimeField(auto_now_add=True)
    unidades = models.IntegerField()
    estado = models.CharField(max_length=45)
    producto_fabrica = models.ForeignKey("ProductoFabrica", on_delete=models.CASCADE)
    usuario = models.ForeignKey("Usuario", on_delete=models.CASCADE)

    def __str__(self):
        return 'CargarArticulo #' + self.id
