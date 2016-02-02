from rest_framework import permissions


class IsOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        # Permissions are only allowed to the owner of the bet ticket
        return obj.owner == request.user
