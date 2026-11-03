from .models import LoginHistory


class AuditMiddleware:
    """Record every login/logout attempt to LoginHistory."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        # session is only available after auth middleware
        user = getattr(request, "user", None)
        if user and user.is_authenticated:
            # record login session once per session id
            from django.contrib.auth.signals import user_logged_in
            # We log in a separate signal handler (signals.py).
        return response


def log_login(sender, request, user, **kwargs):
    ip = (
        request.META.get("HTTP_X_FORWARDED_FOR", "").split(",")[0].strip()
        or request.META.get("REMOTE_ADDR")
    )
    ua = request.META.get("HTTP_USER_AGENT", "")[:255]
    LoginHistory.objects.create(
        user=user, ip_address=ip, user_agent=ua, was_successful=True,
    )


def log_login_failed(sender, credentials, request, **kwargs):
    from django.contrib.auth import get_user_model
    User = get_user_model()
    username = credentials.get("username") if credentials else None
    if username:
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return
        ip = (
            request.META.get("HTTP_X_FORWARDED_FOR", "").split(",")[0].strip()
            if request else None
        ) or (request.META.get("REMOTE_ADDR") if request else None)
        ua = request.META.get("HTTP_USER_AGENT", "")[:255] if request else ""
        LoginHistory.objects.create(
            user=user, ip_address=ip, user_agent=ua, was_successful=False,
        )
