from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, View
from django.http import JsonResponse, HttpResponseRedirect
from django.utils import timezone
from .models import Notification


class NotificationListView(LoginRequiredMixin, ListView):
    model = Notification
    template_name = "notifications/notification_list.html"
    paginate_by = 30
    context_object_name = "notifications"

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by("-created_at")

    def get_context_data(self, **kw):
        ctx = super().get_context_data(**kw)
        ctx["segment"] = "notifications"
        return ctx


class NotificationMarkReadView(LoginRequiredMixin, View):
    def post(self, request, pk):
        n = Notification.objects.filter(pk=pk, user=request.user).first()
        if n:
            n.is_read = True
            n.save(update_fields=["is_read"])
        return JsonResponse({"ok": True})


class NotificationMarkAllReadView(LoginRequiredMixin, View):
    def post(self, request):
        Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
        return JsonResponse({"ok": True})


class NotificationGenerateView(LoginRequiredMixin, View):
    """Trigger scan of low stock, pending requirements, overdue follow-ups."""
    def get(self, request):
        from products.models import Product
        from django.db.models import F
        from crm.models import Call
        from requirements_app.models import Requirement
        today = timezone.localdate()
        # Low stock
        for p in Product.objects.filter(current_stock__lte=F("minimum_stock")):
            Notification.objects.get_or_create(
                notif_type="low_stock", title=f"Low stock: {p.name}",
                message=f"Stock of {p.name} ({p.code}) is {p.current_stock}, below minimum {p.minimum_stock}.",
                url=f"/products/{p.id}/",
                defaults={"user": request.user},
            )
        # Pending requirements
        for r in Requirement.objects.filter(status="new"):
            Notification.objects.get_or_create(
                notif_type="pending_requirement", title=f"New requirement: {r.requirement_number}",
                message=f"Requirement {r.requirement_number} from {r.company} pending.",
                url=f"/requirements/{r.id}/",
                defaults={"user": request.user},
            )
        # Overdue follow-ups
        for c in Call.objects.filter(next_follow_up__lte=today, status="follow_up_pending"):
            Notification.objects.get_or_create(
                notif_type="follow_up_reminder", title=f"Follow-up due: {c.company}",
                message=f"Follow-up for {c.company} on call {c.call_id} is overdue.",
                url=f"/calls/{c.id}/",
                defaults={"user": request.user},
            )
        return HttpResponseRedirect("/notifications/")
