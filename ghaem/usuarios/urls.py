from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EmpleadosDeSucursalViewSet

from .views import (
    SucursalViewSet,
    UserViewSet,
    LoginView,
    PerfilView,
    DashboardGerenteApiView,
    DashboardEncargadoApiView,
    DashboardEmpleadoApiView,
    AsistenciaView,
    AsistenciasTodasView,
    EmpleadosListView,
    EmpleadoDetailView,
    EmpleadosListCreateView,
    SolicitudDiaEmpleadoView, 
    SolicitudDiaGerenteView,
    AsistenciaEmpleadoView,
    DashboardGerenteStatsView,
    AsistenciasEncargadoView
)

router = DefaultRouter()
router.register(r'sucursales', SucursalViewSet, basename='sucursal')
router.register(r'todos', UserViewSet, basename='empleados-todos')  # <-- línea corregida
router.register(r'empleados', EmpleadosDeSucursalViewSet, basename='empleados')

urlpatterns = [
    path('', include(router.urls)),
    path('login/', LoginView.as_view(), name='login'),
    path('perfil/', PerfilView.as_view(), name='perfil'),
    path('dashboard/gerente/', DashboardGerenteApiView.as_view(), name='dashboard-gerente'),
    path('dashboard/encargado/', DashboardEncargadoApiView.as_view(), name='dashboard-encargado'),
    path('dashboard/empleado/', DashboardEmpleadoApiView.as_view(), name='dashboard-empleado'),

    path('dashboard-gerente-stats/', DashboardGerenteStatsView.as_view(), name='dashboard-gerente-stats'),
    path('asistencia/', AsistenciaView.as_view(), name='asistencia'),
    path('asistencias-todas/', AsistenciasTodasView.as_view(), name='asistencias-todas'),

    # Vista de empleados
    path('empleados/', EmpleadosListCreateView.as_view(), name='empleados-list-create'),
    path('empleados/<int:id>/', EmpleadoDetailView.as_view(), name='empleado-detail'),
    path('asistencias/mis-asistencias/', AsistenciaEmpleadoView.as_view(), name='asistencias_empleado'),


    # Solicitudes
    path('solicitudes/', SolicitudDiaEmpleadoView.as_view(), name='solicitudes-empleado'),
    path('solicitudes-gerente/', SolicitudDiaGerenteView.as_view(), name='solicitudes-gerente'),
    path('solicitudes-gerente/<int:pk>/', SolicitudDiaGerenteView.as_view(), name='solicitudes-aprobar-rechazar'),

    path('asistencia/', AsistenciaView.as_view(), name='asistencia'),
    path('asistencias-todas/', AsistenciasTodasView.as_view(), name='asistencias-todas'),
    path('asistencias/encargado/', AsistenciasEncargadoView.as_view(), name='asistencias-encargado'),

]
