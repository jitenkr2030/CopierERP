from .models import AuditLog


def log_action(user, action, model_name, object_id="", object_repr="",
               description="", changes=None, request=None):
    ip = None
    if request is not None:
        ip = (request.META.get("HTTP_X_FORWARDED_FOR", "").split(",")[0].strip()
              or request.META.get("REMOTE_ADDR"))
    AuditLog.objects.create(
        user=user, action=action, model_name=model_name, object_id=str(object_id),
        object_repr=str(object_repr)[:255], description=description,
        changes=changes or {}, ip_address=ip,
    )
