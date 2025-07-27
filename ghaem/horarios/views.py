from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Horario, DIAS_SEMANA
from .serializers import HorarioSerializer
from usuarios.models import User

class IsEncargadoSucursal(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.rol == 'encargado'
    def has_object_permission(self, request, view, obj):
        return (
            obj.empleado.rol in ['empleado', 'encargado'] and
            obj.sucursal in request.user.sucursales.all()
        )

class HorarioViewSet(viewsets.ModelViewSet):
    queryset = Horario.objects.all()
    serializer_class = HorarioSerializer
    permission_classes = [permissions.IsAuthenticated, IsEncargadoSucursal]

    def get_queryset(self):
        qs = super().get_queryset()
        empleado = self.request.query_params.get('empleado')
        sucursal = self.request.query_params.get('sucursal')
        if empleado:
            qs = qs.filter(empleado_id=empleado)
        if sucursal:
            qs = qs.filter(sucursal_id=sucursal)
        return qs

    @action(detail=False, methods=["get"])
    def semana(self, request):
        sucursal_id = request.query_params.get('sucursal')
        if not sucursal_id:
            return Response({'error': 'Debe indicar la sucursal'}, status=400)
        try:
            sucursal_id = int(sucursal_id)
        except:
            return Response({'error': 'ID de sucursal inválido'}, status=400)
        
        if sucursal_id not in [s.id for s in request.user.sucursales.all()]:
            return Response({'error': 'Solo puedes consultar tus sucursales.'}, status=403)

        empleados = User.objects.filter(
            sucursales__id=sucursal_id,
            rol__in=["empleado", "encargado"]
        ).distinct()
        dias = [d[0] for d in DIAS_SEMANA]  # ["lunes", "martes", ...]
        data = []
        for emp in empleados:
            fila = {"nombre": emp.nombre}
            for d in dias:
                # ¿Tiene horario para este día en ESTA sucursal?
                horario = Horario.objects.filter(
                    empleado=emp,
                    sucursal__id=sucursal_id,
                    dia=d
                ).first()
                if horario:
                    fila[d] = f"{horario.hora_entrada.strftime('%I:%M %p').lstrip('0').replace('AM','a.m').replace('PM','p.m')} - {horario.hora_salida.strftime('%I:%M %p').lstrip('0').replace('AM','a.m').replace('PM','p.m')}"
                else:
                    # ¿Tiene horario para este día en OTRA sucursal?
                    otro = Horario.objects.filter(
                        empleado=emp,
                        dia=d
                    ).exclude(sucursal__id=sucursal_id).first()
                    if d == "domingo":
                        fila[d] = ""  # Deja vacío el domingo si no tiene nada
                    elif otro:
                        fila[d] = "Ocupado"
                    else:
                        fila[d] = ""
            data.append(fila)
        return Response(data)
