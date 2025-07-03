from django.db import models

# Create your models here.
class Recurso(models.Model):
    nombre = models.CharField(max_length=200)
    ubicacion = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    capacidad = models.PositiveIntegerField()

    def __str__(self):
        return self.nombre