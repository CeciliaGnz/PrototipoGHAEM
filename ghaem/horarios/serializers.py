from rest_framework import serializers
from .models import Horario

class HorarioSerializer(serializers.ModelSerializer):
    empleado_nombre = serializers.CharField(source='empleado.nombre', read_only=True)
    sucursal_nombre = serializers.CharField(source='sucursal.nombre', read_only=True)

    class Meta:
        model = Horario
        fields = [
            'id',
            'empleado', 'empleado_nombre',
            'sucursal', 'sucursal_nombre',
            'dia',
            'hora_entrada', 'hora_salida'
        ]

    def validate(self, data):
        hora_entrada = data['hora_entrada']
        hora_salida = data['hora_salida']
        empleado = data['empleado']
        sucursal = data['sucursal']
        dia = data['dia']

        # Validar hora entrada < salida
        if hora_entrada >= hora_salida:
            raise serializers.ValidationError("La hora de entrada debe ser antes que la de salida.")

        # Solo debe rechazar traslapes en la MISMA sucursal/día
        conflicto = Horario.objects.filter(
            empleado=empleado,
            sucursal=sucursal,
            dia=dia
        ).exclude(id=self.instance.id if self.instance else None)

        for h in conflicto:
            if (hora_entrada < h.hora_salida and hora_salida > h.hora_entrada):
                raise serializers.ValidationError(
                    f"Ya existe un bloque en {h.sucursal.nombre} ese día que traslapa con ese horario ({h.hora_entrada}-{h.hora_salida})"
                )

        return data
