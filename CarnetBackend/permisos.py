from rest_framework.permissions import BasePermission
from .models import Conferencista, Alumno


class IsOwnerPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Maestros').exists() or request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        return obj.impartidor == Conferencista.objects.get(
            usuario=request.user)


class IsSelf(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            return request.user.is_superuser
        return True

    def has_object_permission(self, request, view, obj):
        if request.method == 'DELETE':
            return False
        return request.user.is_superuser or obj.usuario == request.user


class IsOwnAsistencia(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            return request.user.is_superuser
        return request.user.groups.filter(name='Alumnos').exists() or request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        if request.method in ['DELETE', 'PUT', 'PATCH']:
            return False
        return request.user.is_superuser or obj.alumno == Alumno.objects.get(usuario=request.user)
