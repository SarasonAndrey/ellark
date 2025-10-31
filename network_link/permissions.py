from rest_framework import permissions


class IsActiveEmployee(permissions.BasePermission):
    """
    Проверяет, что пользователь аутентифицирован и активен.
    """

    def has_permission(self, request, view):
        """
        Проверяет права доступа для запроса.

        Args:
            request (Request): Объект запроса.
            view (View): Объект представления.

        Returns:
            bool: True, если пользователь аутентифицирован и активен.
        """
        return request.user.is_authenticated and request.user.is_active
