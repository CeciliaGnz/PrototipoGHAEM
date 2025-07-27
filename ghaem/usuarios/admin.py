from django.contrib import admin
from django import forms
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import User, Asistencia

from .models import Sucursal

admin.site.register(Sucursal)
# Formulario para crear usuarios desde el admin
class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmar contraseña', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('cedula', 'nombre', 'rol')

    def clean_password2(self):
        if self.cleaned_data.get("password1") != self.cleaned_data.get("password2"):
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return self.cleaned_data.get("password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

# Admin de usuarios

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    add_form = UserCreationForm
    list_display = ('cedula', 'nombre', 'rol', 'is_active', 'is_staff')
    list_filter = ('rol', 'is_active')
    search_fields = ('cedula', 'nombre')
    ordering = ('cedula',)
    filter_horizontal = ('groups', 'user_permissions', 'sucursales')  # <- agrega sucursales aquí también

    fieldsets = (
        (None, {'fields': ('cedula', 'password')}),
        ('Información personal', {'fields': ['nombre', 'sucursales']}),  # <--- Aquí
        ('Permisos', {'fields': ('rol', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('cedula', 'nombre', 'rol', 'sucursales', 'password1', 'password2'),  # <--- Aquí
        }),
    )
    
    list_display = ('cedula', 'nombre', 'rol', 'mostrar_sucursales', 'is_active', 'is_staff')
    def mostrar_sucursales(self, obj):
        return ', '.join([s.nombre for s in obj.sucursales.all()])
    mostrar_sucursales.short_description = 'Sucursales'

# Admin de asistencias
@admin.register(Asistencia)
class AsistenciaAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'cedula', 'nombre', 'rol', 'tipo', 'fecha', 'hora', 'estado')  # <- aquí
    list_filter = ('tipo', 'fecha', 'usuario__rol', 'estado')  # <- aquí si quieres filtrar por estado
    search_fields = ('usuario__cedula', 'usuario__nombre')
    date_hierarchy = 'fecha'
    ordering = ('-fecha', '-hora')

    def cedula(self, obj):
        return obj.usuario.cedula
    cedula.short_description = "Cédula"

    def nombre(self, obj):
        return obj.usuario.nombre
    nombre.short_description = "Nombre"

    def rol(self, obj):
        return obj.usuario.rol
    rol.short_description = "Rol"
