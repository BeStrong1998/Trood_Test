from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission): #чтобы все фрагменты кода были видны всем, но также чтобы убедиться, что только пользователь, создавший фрагмент кода, может обновить или удалить его.
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owvner == request.user
        