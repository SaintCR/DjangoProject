from django.db import models

class Cargo(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.CharField(max_length=255)
    descuento = models.BigIntegerField()
    class Meta:
        db_table= 'cargo'

class Clientes(models.Model):
    nombres= models.CharField(max_length=255)
    apellidos= models.CharField(max_length=255)
    telefono = models.CharField(max_length=20)
    direccion = models.CharField(max_length=255)
    correoelectronico = models.CharField(max_length=255)
    cargo = models.ForeignKey(Cargo,on_delete=models.CASCADE)
    class Meta:
        db_table= 'clientes'

class Producto(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.CharField(max_length=255)
    precio = models.BigIntegerField()
    cantidad = models.BigIntegerField()
    foto_url = models.CharField(max_length=255)
    class Meta:
        db_table = 'producto'


class Factura(models.Model):
    fecha = models.CharField(max_length=30)
    total = models.BigIntegerField()
    cliente = models.ForeignKey(Clientes, on_delete=models.CASCADE)

    class Meta:
        db_table = 'factura'


class FacturaHasProducto(models.Model):
    cantidad = models.BigIntegerField()
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, null=True)
    class Meta:
        db_table = 'facturahasproducto'