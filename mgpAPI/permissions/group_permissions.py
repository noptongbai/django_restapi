from rest_framework import permissions


class HasGroupPermission(permissions.BasePermission):
    """
    Ensure user is in required groups.
    """

    def has_permission(self, request, view):
        # Get a mapping of methods -> required group.

        required_permissions_mapping = getattr(view, 'required_permissions', {})

        # Determine the required groups for this particular request method.
        required_permissions = required_permissions_mapping.get(request.method, [])

        # Return True if the user has all the required groups.
        group_all = request.user.groups.all()
        for permission_need in required_permissions:
            for group in group_all:
                for permission in group.permissions.all():
                    if permission_need == permission.codename:
                        return True
        return False
