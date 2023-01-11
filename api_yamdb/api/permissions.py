from rest_framework import permissions
from reviews.models import User


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.author == request.user


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Редактировать объект может только администратор.
    Безопасные методы доступны всем пользователям.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        if not request.user.is_anonymous:
            role = request.user.role
            return role == User.admin


class IsAdmin(permissions.BasePermission):
    """
    Все права эндпоинта только у администратора.
    """
    def has_permission(self, request, view):
        if not request.user.is_anonymous:
            if request.user.is_superuser:
                return True
            role = request.user.role
            return role == User.admin


class AdminModeratorAuthorPermission(permissions.BasePermission):
    """
    Редактировать объект могут только админ, модератор и автор
    Безопасные методы доступны всем пользователям.
    """
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or request.user.role == User.moderator
            or request.user.role == User.admin
        )
