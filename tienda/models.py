from django.db import models

# rol
class Rol(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre

# usuario
class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

# región
class Region(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

# comuna
class Comuna(models.Model):
    nombre = models.CharField(max_length=100)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

# dirección
class Direccion(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    calle = models.CharField(max_length=255)
    numero = models.CharField(max_length=20)
    comuna = models.ForeignKey(Comuna, on_delete=models.CASCADE)
    codigo_postal = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.calle} {self.numero}, {self.comuna.nombre}"

# teléfono
class Telefono(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    numero = models.CharField(max_length=20)

    def __str__(self):
        return self.numero

# categoría
class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to='categorias/', blank=True, null=True)  

    def __str__(self):
        return self.nombre

# unidad de medida
class UnidadMedida(models.Model):
    unidad_medida = models.CharField(max_length=20)
    descripcion = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

# Tabla Producto
class Producto(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    precio = models.FloatField()
    stock = models.IntegerField()
    precio_venta = models.IntegerField()
    precio_compra = models.IntegerField()
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    unidad_medida = models.ForeignKey(UnidadMedida, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)
    def __str__(self):
        return self.nombre

# carrito
class Carrito(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    fecha_creacion = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Carrito de {self.usuario.nombre}"

# ItemCarrito
class ItemCarrito(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre}"

# pedido
class Pedido(models.Model):
    cliente = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha = models.DateField(auto_now_add=True)
    estado = models.CharField(max_length=50)
    total = models.FloatField()

    def __str__(self):
        return f"Pedido #{self.id} de {self.cliente.nombre}"

# DetallePedido
class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio_unitario = models.FloatField()

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre} en pedido #{self.pedido.id}"

# método de pago
class MetodoPago(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre

# pago
class Pago(models.Model):
    pedido = models.OneToOneField(Pedido, on_delete=models.CASCADE)
    metodo_pago = models.ForeignKey(MetodoPago, on_delete=models.CASCADE)
    estado = models.CharField(max_length=50)
    fecha_pago = models.DateField()

    def __str__(self):
        return f"Pago de pedido #{self.pedido.id} - {self.metodo_pago.nombre}"
