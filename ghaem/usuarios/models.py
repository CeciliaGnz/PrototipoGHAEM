from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.conf import settings

ROLES = (
    ('gerente', 'Gerente'),
    ('encargado', 'Encargado'),
    ('empleado', 'Empleado'),
)

class Sucursal(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre

class UserManager(BaseUserManager):
    def create_user(self, cedula, password=None, nombre=None, rol='empleado', **extra_fields):
        if not cedula:
            raise ValueError('La cédula es obligatoria')
        if not nombre:
            raise ValueError('El nombre es obligatorio')
        user = self.model(cedula=cedula, nombre=nombre, rol=rol, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, cedula, password, nombre="Admin", rol='gerente', **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(cedula, password, nombre, rol, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    cedula = models.CharField(max_length=15, unique=True)
    nombre = models.CharField(max_length=100)
    rol = models.CharField(max_length=10, choices=ROLES, default='empleado')
    hora_esperada_entrada = models.TimeField(null=True, blank=True)  # ⏰ Nuevo campo

    sucursales = models.ManyToManyField(Sucursal, blank=True)  # SOLO UNA VEZ

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'cedula'
    REQUIRED_FIELDS = ['nombre', 'rol']

    def __str__(self):
        return f"{self.nombre} ({self.cedula})"

class Asistencia(models.Model):
    TIPO_CHOICES = (
        ('entrada', 'Hora de entrada'),
        ('salida', 'Hora de salida'),
    )
    ESTADO_CHOICES = (
        ('puntual', 'Puntual'),
        ('tarde', 'Tarde'),
        ('temprano', 'Temprano'),
        ('fuera_de_horario', 'Fuera de horario'),
        ('sin_horario', 'Sin horario'),
        ('', 'No aplica'),
    )
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, blank=True, default='')

    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    fecha = models.DateField(auto_now_add=True)
    hora = models.TimeField()
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)

    class Meta:
        unique_together = ('usuario', 'fecha', 'tipo')  # 🔐 evita duplicados

    def __str__(self):
        return f"{self.usuario.cedula} - {self.tipo} - {self.fecha} {self.hora}"
    

# MODEL DE SOLICITUDES
ESTADOS = (
    ('pendiente', 'En espera'),
    ('aprobado', 'Aprobada'),
    ('rechazado', 'Rechazada'),
)

class SolicitudDia(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    motivo = models.TextField()
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    estado = models.CharField(max_length=10, choices=ESTADOS, default='pendiente')
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.nombre} - {self.motivo} ({self.estado})"
