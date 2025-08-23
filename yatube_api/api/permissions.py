from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Разрешение, позволяющее только автору объекта
    редактировать или удалять его.

    Неавторизованные пользователи могут только просматривать контент.
    Авторизованные пользователи могут создавать новый контент.
    Только автор может изменять или удалять свой контент.
    """

    def has_permission(self, request, view):
        """Проверяет общие права доступа для запроса."""
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        """Проверяет права доступа к конкретному объекту."""
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
        )
