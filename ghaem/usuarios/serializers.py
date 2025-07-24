from rest_framework import serializers
from .models import User
from .models import Asistencia
from .models import SolicitudDia

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'cedula', 'nombre', 'rol']

# Para registro de usuarios si quieres (puedes omitir si solo haces login)
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('cedula', 'nombre', 'password', 'rol')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            cedula=validated_data['cedula'],
            nombre=validated_data['nombre'],
            password=validated_data['password'],
            rol=validated_data.get('rol', 'empleado')
        )
        return user

class AsistenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asistencia
        fields = ['id', 'usuario', 'fecha', 'hora', 'tipo']
        read_only_fields = ['usuario', 'fecha', 'hora']


#SOLICITUD DE DIAS
class SolicitudDiaSerializer(serializers.ModelSerializer):
    nombre = serializers.CharField(source='usuario.nombre', read_only=True)
    rol = serializers.CharField(source='usuario.rol', read_only=True)

    class Meta:
        model = SolicitudDia
        fields = ['id', 'usuario', 'nombre', 'rol', 'motivo', 'fecha_inicio', 'fecha_fin', 'estado', 'creado_en']
        read_only_fields = ['usuario', 'estado', 'creado_en']