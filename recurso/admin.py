from django.contrib import admin

from recurso.models import Recurso

# Register your models here.
@admin.register(Recurso) 
class RecursoAdmin(admin.ModelAdmin):
    list_display = ["nombre", "ubicacion", "capacidad"]