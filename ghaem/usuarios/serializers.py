from rest_framework import serializers
from .models import Asistencia, User, Sucursal

from rest_framework import serializers
from .models import User, Sucursal

class UserSerializer(serializers.ModelSerializer):
    sucursales = serializers.PrimaryKeyRelatedField(
        queryset=Sucursal.objects.all(),
        many=True,
        required=False
    )
    sucursal_nombres = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'cedula', 'nombre', 'rol', 'sucursales', 'sucursal_nombres']

    def get_sucursal_nombres(self, obj):
        return [s.nombre for s in obj.sucursales.all()]

# Para registro de usuarios si quieres (puedes omitir si solo haces login)
class RegisterSerializer(serializers.ModelSerializer):
    sucursales = serializers.PrimaryKeyRelatedField(
        queryset=Sucursal.objects.all(),
        many=True,
        required=False
    )

    class Meta:
        model = User
        fields = ('cedula', 'nombre', 'password', 'sucursales', 'rol')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        sucursales = validated_data.pop('sucursales', [])
        user = User.objects.create_user(
            cedula=validated_data['cedula'],
            nombre=validated_data['nombre'],
            password=validated_data['password'],
            rol=validated_data.get('rol', 'empleado')
        )
        user.sucursales.set(sucursales)
        return user

class AsistenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asistencia
        fields = ['id', 'usuario', 'fecha', 'hora', 'tipo']
        read_only_fields = ['usuario', 'fecha', 'hora']

class SucursalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sucursal
        fields = ['id', 'nombre']
