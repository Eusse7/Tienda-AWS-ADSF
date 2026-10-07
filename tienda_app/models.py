from django.db import models

class Libro(models.Model):
    titulo = models.CharField(max_length=200)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock_actual = models.IntegerField(default=0)

class Orden(models.Model):
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE)
    direccion_envio = models.CharField(max_length=200)
    total = models.DecimalField(max_digits=10, decimal_places=2)
