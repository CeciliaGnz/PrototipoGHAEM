from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

ROLES = (
    ('gerente', 'Gerente'),
    ('encargado', 'Encargado'),
    ('empleado', 'Empleado'),
)

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
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'cedula'
    REQUIRED_FIELDS = ['nombre', 'rol']

    def __str__(self):
        return f"{self.nombre} ({self.cedula})"
