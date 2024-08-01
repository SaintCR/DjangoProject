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