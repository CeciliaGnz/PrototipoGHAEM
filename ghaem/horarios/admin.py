from django.contrib import admin
from .models import Horario

@admin.register(Horario)
class HorarioAdmin(admin.ModelAdmin):
    list_display = ('empleado', 'sucursal', 'dia', 'hora_entrada', 'hora_salida')
    list_filter = ('sucursal', 'dia')
    search_fields = ('empleado__nombre', 'empleado__cedula', 'sucursal__nombre')
    ordering = ('empleado', 'dia')