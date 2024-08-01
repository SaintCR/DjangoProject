from django.db import models

class Cargo(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.CharField(max_length=255)
    descuento = models.BigIntegerField()
    class Meta:
        db_table= 'cargo'