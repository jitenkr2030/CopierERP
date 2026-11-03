from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from .models import AuditLog, TransactionLog


class AuditLogListView(LoginRequiredMixin, ListView):
    model = AuditLog
    template_name = "audit/audit_log_list.html"
    paginate_by = 50
    context_object_name = "logs"

    def get_queryset(self):
        qs = AuditLog.objects.select_related("user")
        action = self.request.GET.get("action")
        if action:
            qs = qs.filter(action=action)
        model_name = self.request.GET.get("model")
        if model_name:
            qs = qs.filter(model_name__icontains=model_name)
        return qs

    def get_context_data(self, **kw):
        ctx = super().get_context_data(**kw)
        ctx["segment"] = "audit"
        ctx["action_choices"] = AuditLog.ACTION_CHOICES
        return ctx


class TransactionLogListView(LoginRequiredMixin, ListView):
    model = TransactionLog
    template_name = "audit/transaction_log_list.html"
    paginate_by = 50
    context_object_name = "logs"

    def get_queryset(self):
        return TransactionLog.objects.select_related("user").order_by("-created_at")

    def get_context_data(self, **kw):
        ctx = super().get_context_data(**kw)
        ctx["segment"] = "audit"
        return ctx
