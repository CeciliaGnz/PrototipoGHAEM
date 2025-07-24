from django.urls import path
from .views import (
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
    SolicitudDiaEmpleadoView,  # <-- Añade esto
    SolicitudDiaGerenteView,
    AsistenciaEmpleadoView,
)

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('perfil/', PerfilView.as_view(), name='perfil'),

    # Dashboards protegidos por rol
    path('dashboard/gerente/', DashboardGerenteApiView.as_view(), name='dashboard-gerente'),
    path('dashboard/encargado/', DashboardEncargadoApiView.as_view(), name='dashboard-encargado'),
    path('dashboard/empleado/', DashboardEmpleadoApiView.as_view(), name='dashboard-empleado'),

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
]
