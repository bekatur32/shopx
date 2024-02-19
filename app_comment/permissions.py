from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsClientOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            # Проверяем, является ли пользователь администратором или клиентом
            if request.user.is_superuser or request.user.is_staff or hasattr(request.user, 'is_client'):
                return True
            # Если пользователь не администратор или клиент, проверяем, является ли он владельцем объекта
            return obj.user == request.user
        return False