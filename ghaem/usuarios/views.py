from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

from .permissions import IsGerente, IsEncargado, IsEmpleado


from .models import User
from .serializers import UserSerializer, RegisterSerializer

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        cedula = request.data.get('cedula')
        password = request.data.get('password')
        user = authenticate(request, cedula=cedula, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            user_data = UserSerializer(user).data
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'user': user_data
            })
        return Response({'error': 'Credenciales inválidas'}, status=400)

class PerfilView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response(UserSerializer(user).data)

class AlgoProtegidoView(APIView):
    permission_classes = [IsAuthenticated]


class DashboardGerenteApiView(APIView):
    permission_classes = [IsAuthenticated, IsGerente]
    def get(self, request):
        return Response({"mensaje": "Solo gerente puede ver esto"})

class DashboardEncargadoApiView(APIView):
    permission_classes = [IsAuthenticated, IsEncargado]
    def get(self, request):
        return Response({"mensaje": "Solo encargado puede ver esto"})

class DashboardEmpleadoApiView(APIView):
    permission_classes = [IsAuthenticated, IsEmpleado]
    def get(self, request):
        return Response({"mensaje": "Solo empleado puede ver esto"})