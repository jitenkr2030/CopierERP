from django.contrib.auth.signals import user_logged_in, user_login_failed
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User
from .middleware import log_login, log_login_failed


user_logged_in.connect(log_login)
user_login_failed.connect(log_login_failed)


@receiver(post_save, sender=User)
def ensure_employee_id(sender, instance, created, **kwargs):
    if created and not instance.employee_id:
        prefix = "EMP"
        last_id = User.objects.exclude(employee_id__isnull=True).count() + 1
        instance.employee_id = f"{prefix}-{last_id:04d}"
        User.objects.filter(pk=instance.pk).update(employee_id=instance.employee_id)
