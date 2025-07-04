from rest_framework import serializers
from .models import User

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
