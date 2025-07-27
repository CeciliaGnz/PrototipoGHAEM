from django.db import models
from usuarios.models import User, Sucursal  # Ajusta el import según tu estructura

DIAS_SEMANA = [
    ('lunes', 'Lunes'),
    ('martes', 'Martes'),
    ('miercoles', 'Miércoles'),
    ('jueves', 'Jueves'),
    ('viernes', 'Viernes'),
    ('sabado', 'Sábado'),
    ('domingo', 'Domingo'),
]

class Horario(models.Model):
    empleado = models.ForeignKey(User, on_delete=models.CASCADE, related_name="horarios")
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE)
    dia = models.CharField(max_length=10, choices=DIAS_SEMANA)
    hora_entrada = models.TimeField()
    hora_salida = models.TimeField()

    class Meta:
        unique_together = ('empleado', 'sucursal', 'dia')

    def __str__(self):
        return f"{self.empleado.nombre} - {self.dia}: {self.hora_entrada} a {self.hora_salida} ({self.sucursal.nombre})"