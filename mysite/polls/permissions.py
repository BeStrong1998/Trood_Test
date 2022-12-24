from rest_framework import permissions


"""чтобы все фрагменты когда были видны всем, но также чтобы убедиться,
что только пользователь, создавший фрагмент кода,
может обновить или удалить его."""


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owvner == request.user
