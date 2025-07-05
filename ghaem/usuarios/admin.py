from django.contrib import admin
from .models import User, Asistencia

@admin.register(Asistencia)
class AsistenciaAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'cedula', 'nombre', 'tipo', 'fecha', 'hora')
    list_filter = ('tipo', 'fecha', 'usuario__rol')
    search_fields = ('usuario__cedula', 'usuario__nombre')
    date_hierarchy = 'fecha'
    ordering = ('-fecha', '-hora')

    # Mostrar cédula y nombre directamente en la tabla
    def cedula(self, obj):
        return obj.usuario.cedula
    cedula.short_description = "Cédula"

    def nombre(self, obj):
        return obj.usuario.nombre
    nombre.short_description = "Nombre"

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('cedula', 'nombre', 'rol', 'is_active', 'is_staff')
    list_filter = ('rol', 'is_active')
    search_fields = ('cedula', 'nombre')
