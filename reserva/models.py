from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User

from recurso.models import Recurso

# Create your models here.
class Reserva(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuario", null=True, blank=True)
    fecha_hora = models.DateTimeField(default=timezone.now)
    recurso = models.ForeignKey(Recurso, on_delete=models.CASCADE, null=True, blank=True)


    def __str__(self):
        return f"{self.user} - {self.fecha_hora}"