from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import (
    status, permissions, serializers, generics, viewsets
)
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from django.utils import timezone
from django.utils.timezone import localtime, now, localdate
from django.db import IntegrityError
from .models import Asistencia
from .serializers import AsistenciaSerializer
from rest_framework import serializers
from rest_framework import generics 
from .models import SolicitudDia
from .serializers import SolicitudDiaSerializer

from collections import defaultdict
from rest_framework import viewsets, permissions
from .models import User, Sucursal
from .serializers import UserSerializer, SucursalSerializer

from datetime import timedelta
from django.utils.timezone import localdate
from django.db.models import F, ExpressionWrapper, TimeField
from datetime import datetime, timedelta, time
from horarios.models import Horario

# Modelos y Serializers de tu app
from .models import Asistencia, User, Sucursal, SolicitudDia
from .serializers import (
    AsistenciaSerializer,
    UserSerializer,
    RegisterSerializer,
    SucursalSerializer,
    SolicitudDiaSerializer,
)
from .permissions import IsGerente, IsEncargado, IsEmpleado


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

    def post(self, request):
        tipo = request.data.get('tipo')
        sucursal_id = request.data.get('sucursal')
        
        if tipo not in ['entrada', 'salida']:
            return Response({'error': 'Tipo inválido'}, status=400)

        hoy = timezone.localtime().date()
        usuario = request.user

        if tipo == 'salida':
            if not Asistencia.objects.filter(usuario=usuario, tipo='entrada', fecha=hoy).exists():
                return Response({'error': 'No puedes marcar salida sin haber registrado la entrada primero.'}, status=400)

            if Asistencia.objects.filter(usuario=usuario, tipo='salida', fecha=hoy).exists():
                return Response({'mensaje': 'Ya marcaste salida hoy'}, status=200)

        if tipo == 'entrada':
            if Asistencia.objects.filter(usuario=usuario, tipo='entrada', fecha=hoy).exists():
                return Response({'mensaje': f'Ya marcaste {tipo} hoy'}, status=200)
            
        # Lógica de estado
        dias = ['lunes', 'martes', 'miercoles', 'jueves', 'viernes', 'sabado', 'domingo']
        dia_hoy = dias[localtime().weekday()]
        horario = Horario.objects.filter(
            empleado=usuario,
            sucursal_id=sucursal_id,
            dia=dia_hoy
        ).first()
        hora_actual = localtime().time()
        estado = ""

        if horario:
            tolerancia = timedelta(minutes=15)
            entrada_limite = (datetime.combine(hoy, horario.hora_entrada) + tolerancia).time()
            if tipo == "entrada":
                if hora_actual > entrada_limite:
                    estado = "tarde"
                elif hora_actual < horario.hora_entrada:
                    estado = "temprano"
                else:
                    estado = "puntual"
            elif tipo == "salida":
                if hora_actual < horario.hora_salida:
                    estado = "temprano"
                elif hora_actual > horario.hora_salida:
                    estado = "fuera_de_horario"
                else:
                    estado = "puntual"
        else:
            estado = "sin_horario"  # <-- Aquí permites el registro de todos modos


        asistencia = Asistencia.objects.create(
            usuario=request.user,
            tipo=tipo,
            hora=timezone.localtime().time(),
            estado=estado
        )

        serializer = AsistenciaSerializer(asistencia)
        return Response({
            'mensaje': f'{tipo.capitalize()} registrada correctamente.',
            'tipo': tipo,
            'asistencia': serializer.data
        }, status=201)
        

    # Listar asistencias
    def get(self, request):
        asistencias = Asistencia.objects.filter(usuario=request.user).order_by('-fecha', '-hora')
        serializer = AsistenciaSerializer(asistencias, many=True)
        return Response(serializer.data)


# TODAS LAS ASISTENCIAS
class AsistenciasTodasView(APIView):
    permission_classes = [IsAuthenticated, IsGerente]

    def get(self, request):
        asistencias = Asistencia.objects.exclude(usuario__rol='gerente').order_by('-fecha', '-hora')
        serializer = AsistenciaSerializer(asistencias, many=True)
        return Response(serializer.data)
    

# ASISTENCIA DE EMPLEADO PROPIA
class AsistenciaEmpleadoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        usuario = request.user
        asistencias = Asistencia.objects.filter(usuario=usuario).order_by('-fecha', '-hora')
        serializer = AsistenciaSerializer(asistencias, many=True)
        return Response(serializer.data)


# EQUIPO
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

class SucursalViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Sucursal.objects.all()
    serializer_class = SucursalSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class SucursalViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Sucursal.objects.all()
    serializer_class = SucursalSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]



#SOLICITUDES DE DIAS # Crear y listar propias solicitudes
class SolicitudDiaEmpleadoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        solicitudes = SolicitudDia.objects.filter(usuario=request.user).order_by('-creado_en')
        serializer = SolicitudDiaSerializer(solicitudes, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data.copy()
        data['usuario'] = request.user.id
        serializer = SolicitudDiaSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save(usuario=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

# Ver y aprobar/rechazar (solo gerente)
class SolicitudDiaGerenteView(APIView):
    permission_classes = [IsAuthenticated, IsGerente]

    def get(self, request):
        solicitudes = SolicitudDia.objects.all().order_by('-creado_en')
        serializer = SolicitudDiaSerializer(solicitudes, many=True)
        return Response(serializer.data)

    def patch(self, request, pk):
        try:
            solicitud = SolicitudDia.objects.get(pk=pk)
        except SolicitudDia.DoesNotExist:
            return Response({'error': 'Solicitud no encontrada'}, status=404)

        nuevo_estado = request.data.get('estado')
        if nuevo_estado not in ['aprobado', 'rechazado']:
            return Response({'error': 'Estado inválido'}, status=400)

        solicitud.estado = nuevo_estado
        solicitud.save()
        return Response({'mensaje': f'Solicitud {nuevo_estado} correctamente'})
    

# VIEWS DASHBOARD DEL GERENTE
class DashboardGerenteStatsView(APIView):
    permission_classes = [IsAuthenticated, IsGerente]

    def get(self, request):
        hoy = now().date()
        empleados_total = User.objects.filter(rol='empleado').count()
        entradas_hoy = Asistencia.objects.filter(tipo='entrada', fecha=hoy)
        salidas_hoy = Asistencia.objects.filter(tipo='salida', fecha=hoy)
        solicitudes_pendientes = SolicitudDia.objects.filter(estado='pendiente').count()

        llegadas_tarde = 0
        for asistencia in entradas_hoy:
            usuario = asistencia.usuario
            hora_esperada = usuario.hora_esperada_entrada  # asegúrate de que este campo existe
            if hora_esperada:
                tolerancia = (datetime.combine(hoy, hora_esperada) + timedelta(minutes=15)).time()
                if asistencia.hora > tolerancia:
                    llegadas_tarde += 1

        data = {
            'total_empleados': empleados_total,
            'entradas_hoy': entradas_hoy.count(),
            'salidas_hoy': salidas_hoy.count(),
            'llegadas_tarde_hoy': llegadas_tarde,
            'solicitudes_pendientes': solicitudes_pendientes,
        }

        return Response(data)

class EmpleadosDeSucursalViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        usuario = self.request.user
        return User.objects.filter(
            sucursales__in=usuario.sucursales.all(),
            rol__in=["empleado", "encargado"]
        ).distinct()