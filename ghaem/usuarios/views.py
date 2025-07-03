from django.shortcuts import render

# Create your views here.
from rest_framework import generics, status
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Usuario
from .serializers import UsuarioSerializer
from rest_framework.permissions import IsAuthenticated

# Registro de usuario (solo para pruebas, puedes eliminarlo en producción)
class RegistroUsuarioView(generics.CreateAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        rol = request.data.get('rol')
        if Usuario.objects.filter(username=username).exists():
            return Response({'error': 'El usuario ya existe'}, status=400)
        usuario = Usuario.objects.create_user(username=username, password=password, rol=rol)
        return Response(UsuarioSerializer(usuario).data)

# Login
class LoginView(generics.GenericAPIView):
    serializer_class = UsuarioSerializer

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        usuario = authenticate(username=username, password=password)
        if usuario:
            refresh = RefreshToken.for_user(usuario)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': UsuarioSerializer(usuario).data,
            })
        return Response({'error': 'Credenciales inválidas'}, status=401)

# Vista protegida de ejemplo
from rest_framework.views import APIView

class PerfilView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UsuarioSerializer(request.user).data)
