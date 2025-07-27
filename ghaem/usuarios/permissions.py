from rest_framework.permissions import BasePermission

class IsGerente(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.rol == 'gerente'

class IsEncargado(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.rol == 'encargado'

class IsEmpleado(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.rol == 'empleado'
