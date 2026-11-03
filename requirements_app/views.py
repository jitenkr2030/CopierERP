from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.db import transaction

from .models import Requirement, RequirementItem
from .forms import RequirementForm, RequirementItemFormSet
from audit.utils import log_action


class RequirementListView(LoginRequiredMixin, ListView):
    model = Requirement
    template_name = "requirements_app/requirement_list.html"
    paginate_by = 25
    context_object_name = "requirements"

    def get_queryset(self):
        qs = Requirement.objects.select_related("company", "assigned_to")
        status = self.request.GET.get("status")
        if status:
            qs = qs.filter(status=status)
        q = self.request.GET.get("q")
        if q:
            qs = qs.filter(requirement_number__icontains=q) | qs.filter(company__name__icontains=q)
        return qs.order_by("-id")

    def get_context_data(self, **kw):
        ctx = super().get_context_data(**kw)
        ctx["segment"] = "requirements"
        ctx["statuses"] = Requirement.STATUS
        return ctx


class RequirementCreateView(LoginRequiredMixin, CreateView):
    model = Requirement
    form_class = RequirementForm
    template_name = "requirements_app/requirement_form.html"

    def get_context_data(self, **kw):
        ctx = super().get_context_data(**kw)
        ctx["segment"] = "requirements"
        ctx["title"] = "Create Requirement"
        if self.request.POST:
            ctx["items"] = RequirementItemFormSet(self.request.POST)
        else:
            ctx["items"] = RequirementItemFormSet()
        return ctx

    def form_valid(self, form):
        ctx = self.get_context_data()
        items = ctx["items"]
        with transaction.atomic():
            form.instance.created_by = self.request.user
            self.object = form.save()
            items.instance = self.object
            if items.is_valid():
                items.save()
        log_action(self.request.user, "create", "Requirement",
                   self.object.id, str(self.object), "Requirement created", request=self.request)
        return redirect("requirements_app:requirement_detail", pk=self.object.pk)


class RequirementUpdateView(LoginRequiredMixin, UpdateView):
    model = Requirement
    form_class = RequirementForm
    template_name = "requirements_app/requirement_form.html"

    def get_context_data(self, **kw):
        ctx = super().get_context_data(**kw)
        ctx["segment"] = "requirements"
        ctx["title"] = "Edit Requirement"
        if self.request.POST:
            ctx["items"] = RequirementItemFormSet(self.request.POST, instance=self.object)
        else:
            ctx["items"] = RequirementItemFormSet(instance=self.object)
        return ctx

    def form_valid(self, form):
        ctx = self.get_context_data()
        items = ctx["items"]
        with transaction.atomic():
            self.object = form.save()
            if items.is_valid():
                items.save()
        return redirect("requirements_app:requirement_detail", pk=self.object.pk)


class RequirementDetailView(LoginRequiredMixin, DetailView):
    model = Requirement
    template_name = "requirements_app/requirement_detail.html"
    context_object_name = "requirement"

    def get_context_data(self, **kw):
        ctx = super().get_context_data(**kw)
        ctx["segment"] = "requirements"
        return ctx


class RequirementCheckStockView(LoginRequiredMixin, View):
    def get(self, request, pk):
        r = get_object_or_404(Requirement, pk=pk)
        all_available = True
        for it in r.items.all():
            if it.product.current_stock < it.required_qty:
                all_available = False
                break
        r.status = "available" if all_available else "unavailable"
        r.save(update_fields=["status"])
        return redirect("requirements_app:requirement_detail", pk=pk)
