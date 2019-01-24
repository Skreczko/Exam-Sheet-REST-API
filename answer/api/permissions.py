from rest_framework import permissions




class IsOwner(permissions.BasePermission):
    message  = 'You must be the owner of this content to change.'
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user

class IsStaffUser(permissions.BasePermission):
    """
    Allows access only to admin users.
    """

    def has_permission(self, request, view, obj):
        return obj.user.is_staff