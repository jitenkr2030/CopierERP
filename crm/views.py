from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DetailView

from .models import Call, FollowUp
from .forms import CallForm, FollowUpForm


class CallListView(LoginRequiredMixin, ListView):
    model = Call
    template_name = "crm/call_list.html"
    paginate_by = 25
    context_object_name = "calls"

    def get_queryset(self):
        qs = Call.objects.select_related("company", "assigned_to")
        status = self.request.GET.get("status")
        if status:
            qs = qs.filter(status=status)
        q = self.request.GET.get("q")
        if q:
            qs = qs.filter(company__name__icontains=q) | qs.filter(call_id__icontains=q)
        return qs.order_by("-id")

    def get_context_data(self, **kw):
        ctx = super().get_context_data(**kw)
        ctx["segment"] = "crm"
        ctx["statuses"] = Call.CALL_STATUS
        return ctx


class CallCreateView(LoginRequiredMixin, CreateView):
    model = Call
    form_class = CallForm
    template_name = "crm/call_form.html"
    success_url = reverse_lazy("crm:call_list")

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        if not form.instance.assigned_to:
            form.instance.assigned_to = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kw):
        ctx = super().get_context_data(**kw)
        ctx["segment"] = "crm"
        ctx["title"] = "Log Call"
        return ctx


class CallUpdateView(LoginRequiredMixin, UpdateView):
    model = Call
    form_class = CallForm
    template_name = "crm/call_form.html"
    success_url = reverse_lazy("crm:call_list")

    def get_context_data(self, **kw):
        ctx = super().get_context_data(**kw)
        ctx["segment"] = "crm"
        ctx["title"] = "Edit Call"
        return ctx


class CallDetailView(LoginRequiredMixin, DetailView):
    model = Call
    template_name = "crm/call_detail.html"
    context_object_name = "call"

    def get_context_data(self, **kw):
        ctx = super().get_context_data(**kw)
        ctx["segment"] = "crm"
        ctx["followups"] = self.object.followups.select_related("done_by").order_by("-date")
        ctx["followup_form"] = FollowUpForm()
        return ctx


class AddFollowUpView(LoginRequiredMixin, View):
    def post(self, request, pk):
        call = get_object_or_404(Call, pk=pk)
        form = FollowUpForm(request.POST)
        if form.is_valid():
            fu = form.save(commit=False)
            fu.call = call
            fu.done_by = request.user
            fu.save()
            if fu.next_follow_up:
                call.next_follow_up = fu.next_follow_up
                call.status = "follow_up_pending"
                call.save(update_fields=["next_follow_up", "status"])
        return redirect("crm:call_detail", pk=pk)
