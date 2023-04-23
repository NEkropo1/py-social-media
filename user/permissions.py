from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdminOrOwnerOrIfAuthenticatedReadOnly(BasePermission):
    def has_permission(self, request, view, obj=None):
        return bool(
            (
                request.method in SAFE_METHODS
                and request.user
                and request.user.is_authenticated
            )
            or (request.user and request.user.is_staff)
            or (obj and obj.id == request.user.id)
        )


class IsAdminOrIfAuthenticatedReadOnly(BasePermission):
    def has_permission(self, request, view):
        return bool(
            (
                request.method in SAFE_METHODS
                and request.user
                and request.user.is_authenticated
            )
            or (request.user and request.user.is_staff)
        )
