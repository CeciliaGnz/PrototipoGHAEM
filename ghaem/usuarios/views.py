from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from .models import Asistencia
from .serializers import AsistenciaSerializer
from rest_framework import serializers
from rest_framework import generics 




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
    
class AsistenciaView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    # Registrar asistencia
    def post(self, request):
        tipo = request.data.get('tipo')
        if tipo not in ['entrada', 'salida']:
            return Response({'error': 'Tipo inválido'}, status=400)
        
        hoy = timezone.now().date()
        
        if tipo == 'salida':
            # Si NO hay entrada hoy, no puedes marcar salida
            ya_entro = Asistencia.objects.filter(
                usuario=request.user,
                tipo='entrada',
                fecha=hoy
            ).exists()
            if not ya_entro:
                return Response({'error': 'No puedes marcar salida sin haber registrado la entrada primero.'}, status=400)
            
            # Si ya marcó salida hoy, no puedes marcar de nuevo
            ya_marco_salida = Asistencia.objects.filter(
                usuario=request.user,
                tipo='salida',
                fecha=hoy
            ).exists()
            if ya_marco_salida:
                return Response({'error': 'Ya marcaste salida hoy'}, status=400)

        if tipo == 'entrada':
            ya_marcada = Asistencia.objects.filter(
                usuario=request.user,
                tipo='entrada',
                fecha=hoy
            ).exists()
            if ya_marcada:
                return Response({'error': f'Ya marcaste {tipo} hoy'}, status=400)
        
        asistencia = Asistencia.objects.create(
            usuario=request.user,
            tipo=tipo
        )
        serializer = AsistenciaSerializer(asistencia)
        return Response(serializer.data, status=201)

    # Listar asistencias
    def get(self, request):
        asistencias = Asistencia.objects.filter(usuario=request.user).order_by('-fecha', '-hora')
        serializer = AsistenciaSerializer(asistencias, many=True)
        return Response(serializer.data)


#TODAS LAS ASISTENCIAS
class AsistenciaSerializer(serializers.ModelSerializer):
    nombre = serializers.CharField(source='usuario.nombre', read_only=True)
    rol = serializers.CharField(source='usuario.rol', read_only=True)
    hora = serializers.TimeField(format='%H:%M', read_only=True) 
    class Meta:
        model = Asistencia
        fields = ['id', 'tipo', 'fecha', 'hora', 'nombre', 'rol']

    
    
class AsistenciasTodasView(APIView):
    permission_classes = [IsAuthenticated,IsGerente]

    def get(self, request):
        asistencias = Asistencia.objects.exclude(usuario__rol='gerente').order_by('-fecha', '-hora')
        serializer = AsistenciaSerializer(asistencias, many=True)
        return Response(serializer.data)

#EQUIPO
class EmpleadosListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, IsGerente]
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.exclude(rol='gerente')
    
class EmpleadosListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated, IsGerente]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return RegisterSerializer
        return UserSerializer

    def get_queryset(self):
        return User.objects.exclude(rol='gerente')

class EmpleadoDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsGerente]
    serializer_class = UserSerializer
    lookup_field = 'id'

    def get_queryset(self):
        return User.objects.exclude(rol='gerente')
