from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DetailView, TemplateView
from django.utils import timezone
from django.db.models import Sum, Count, Q, F

from .models import User, LoginHistory, ROLE_CHOICES, ROLE_PERMISSIONS
from .forms import LoginForm, UserCreateForm, UserUpdateForm, UserProfileForm


# ---------- 404 / 500 ----------
def handler404(request, exception=None):
    return render(request, "errors/404.html", status=404)


def handler500(request):
    return render(request, "errors/500.html", status=500)


# ---------- Auth ----------
class LoginView(View):
    template_name = "registration/login.html"

    def get(self, request):
        if request.user.is_authenticated:
            return redirect("dashboard")
        return render(request, self.template_name, {"form": LoginForm()})

    def post(self, request):
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect("dashboard")
        return render(request, self.template_name, {"form": form})


class LogoutView(View):
    def get(self, request):
        if request.user.is_authenticated:
            last = LoginHistory.objects.filter(user=request.user).order_by("-login_time").first()
            if last and not last.logout_time:
                last.logout_time = timezone.now()
                last.save(update_fields=["logout_time"])
            auth_logout(request)
        return redirect("login")


@login_required
def dashboard(request):
    """Main dashboard — daily business overview."""
    today = timezone.localdate()
    # Lazy imports to avoid circular imports during initial migration
    from companies.models import Company
    from customers.models import Customer
    from suppliers.models import Supplier
    from products.models import Product
    from purchases.models import Purchase
    from sales.models import Sale
    from stock_issues.models import StockIssue
    from crm.models import Call
    from requirements_app.models import Requirement
    from payments.models import Payment

    low_stock = Product.objects.filter(current_stock__lte=F("minimum_stock"))

    context = {
        "segment": "dashboard",
        "today": today,
        "companies_count": Company.objects.count(),
        "customers_count": Customer.objects.count(),
        "suppliers_count": Supplier.objects.count(),
        "products_count": Product.objects.count(),
        "today_purchases": Purchase.objects.filter(purchase_date=today).count(),
        "today_sales": Sale.objects.filter(sale_date=today).count(),
        "today_stock_issues": StockIssue.objects.filter(issue_date=today).count(),
        "today_calls": Call.objects.filter(call_date=today).count(),
        "pending_followups": Call.objects.filter(
            next_follow_up__lte=today, status="follow_up_pending"
        ).count(),
        "pending_requirements": Requirement.objects.filter(status="new").count(),
        "products_low_count": low_stock.count(),
        "low_stock_list": low_stock[:5],
        "total_stock_qty": Product.objects.aggregate(t=Sum("current_stock"))["t"] or 0,
        "total_stock_value": Product.objects.aggregate(t=Sum(F("current_stock") * F("purchase_rate")))["t"] or 0,
        "recent_purchases": Purchase.objects.select_related("supplier").order_by("-id")[:5],
        "recent_sales": Sale.objects.select_related("customer").order_by("-id")[:5],
        "recent_calls": Call.objects.select_related("company", "assigned_to").order_by("-id")[:5],
        "recent_requirements": Requirement.objects.select_related("company").order_by("-id")[:5],
        "role": request.user.role,
    }
    return render(request, "dashboard.html", context)


class UserListView(LoginRequiredMixin, ListView):
    model = User
    template_name = "accounts/user_list.html"
    paginate_by = 20
    context_object_name = "users"

    def get_queryset(self):
        qs = User.objects.select_related()
        q = self.request.GET.get("q")
        if q:
            qs = qs.filter(Q(username__icontains=q) | Q(email__icontains=q)
                           | Q(first_name__icontains=q) | Q(last_name__icontains=q)
                           | Q(employee_id__icontains=q))
        role = self.request.GET.get("role")
        if role:
            qs = qs.filter(role=role)
        return qs

    def get_context_data(self, **kw):
        ctx = super().get_context_data(**kw)
        ctx["roles"] = ROLE_CHOICES
        ctx["segment"] = "users"
        return ctx


class UserCreateView(LoginRequiredMixin, CreateView):
    model = User
    form_class = UserCreateForm
    template_name = "accounts/user_form.html"
    success_url = reverse_lazy("user_list")

    def get_context_data(self, **kw):
        ctx = super().get_context_data(**kw)
        ctx["segment"] = "users"
        ctx["title"] = "Create User"
        return ctx


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = "accounts/user_form.html"
    success_url = reverse_lazy("user_list")

    def get_context_data(self, **kw):
        ctx = super().get_context_data(**kw)
        ctx["segment"] = "users"
        ctx["title"] = "Edit User"
        return ctx


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = "accounts/user_detail.html"
    context_object_name = "user_obj"

    def get_context_data(self, **kw):
        ctx = super().get_context_data(**kw)
        ctx["segment"] = "users"
        ctx["recent_logins"] = self.object.logins.order_by("-login_time")[:10]
        return ctx


class ProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = "accounts/profile.html"
    success_url = reverse_lazy("profile")

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kw):
        ctx = super().get_context_data(**kw)
        ctx["segment"] = "profile"
        return ctx


class RoleListView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/role_list.html"

    def get_context_data(self, **kw):
        ctx = super().get_context_data(**kw)
        rows = []
        for code, label in ROLE_CHOICES:
            rows.append({
                "code": code,
                "label": label,
                "modules": "*" if "*" in ROLE_PERMISSIONS.get(code, [])
                              else ROLE_PERMISSIONS.get(code, []),
                "user_count": User.objects.filter(role=code).count(),
            })
        ctx["roles"] = rows
        ctx["segment"] = "roles"
        return ctx


class LoginHistoryView(LoginRequiredMixin, ListView):
    model = LoginHistory
    template_name = "accounts/login_history.html"
    paginate_by = 50
    context_object_name = "logins"

    def get_queryset(self):
        return LoginHistory.objects.select_related("user").order_by("-login_time")

    def get_context_data(self, **kw):
        ctx = super().get_context_data(**kw)
        ctx["segment"] = "login_history"
        return ctx
