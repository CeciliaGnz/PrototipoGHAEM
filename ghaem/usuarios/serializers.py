from rest_framework import serializers
from .models import Asistencia, User, Sucursal
from rest_framework import serializers
from .models import SolicitudDia

class UserSerializer(serializers.ModelSerializer):
    sucursales = serializers.PrimaryKeyRelatedField(
        queryset=Sucursal.objects.all(),
        many=True,
        required=False
    )
    sucursal_nombres = serializers.SerializerMethodField()

<<<<<<< HEAD
=======
# Para registro de usuarios
class RegisterSerializer(serializers.ModelSerializer):
>>>>>>> bb75af2 (DASH CARDS POR TERMINAR, MUESTRA SOLO LOS EMPLEADOS EN PANTALLA GERENTE)
    class Meta:
        model = User
        fields = ['id', 'cedula', 'nombre', 'rol', 'sucursales', 'sucursal_nombres']

    def get_sucursal_nombres(self, obj):
        return [s.nombre for s in obj.sucursales.all()]

# Para registro de usuarios
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


#SOLICITUD DE DIAS
class SolicitudDiaSerializer(serializers.ModelSerializer):
    nombre = serializers.CharField(source='usuario.nombre', read_only=True)
    rol = serializers.CharField(source='usuario.rol', read_only=True)

    class Meta:
        model = SolicitudDia
        fields = ['id', 'usuario', 'nombre', 'rol', 'motivo', 'fecha_inicio', 'fecha_fin', 'estado', 'creado_en']
        read_only_fields = ['usuario', 'estado', 'creado_en']

class SucursalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sucursal
        fields = ['id', 'nombre']
