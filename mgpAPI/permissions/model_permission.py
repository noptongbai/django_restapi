from rest_framework.permissions import DjangoModelPermissions

class BaseModelPerm(DjangoModelPermissions):
    def has_permission(self, request, view):
        perms = self.get_required_permissions(request.method, self.models)

        return (
            request.user and
            (request.user.is_authenticated() or not self.authenticated_users_only) and
            request.user.has_perms(perms)
        )

def model_permissions(model_cls, base=BaseModelPerm):
    from rest_framework.decorators import permission_classes
    class DjangoModelPerm(base):
        model = model_cls
    return permission_classes((DjangoModelPerm,))