from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.created_by == request.user


class IsOwner(permissions.BasePermission):
    """
    Permission to only user allow to edit or delete his own profile.
    """
    def has_object_permission(self, request, view, obj):
        return obj.id == request.user.id
