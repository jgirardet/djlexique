from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404


def get_object_if_owner(request, klass, field="user", **kwargs):
    object = get_object_or_404(klass, **kwargs)
    if "." in field:
        sub, field = field.split(".")
        target_user = getattr(object, sub)
    else:
        target_user = object
    if request.user == getattr(target_user, field):
        return object
    raise PermissionDenied()
