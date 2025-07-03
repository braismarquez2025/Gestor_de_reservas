from django.contrib import admin

from reserva.models import Reserva

# Register your models here.
@admin.register(Reserva) 
class ReservaAdmin(admin.ModelAdmin):
    list_display = ["user", "fecha_hora"]