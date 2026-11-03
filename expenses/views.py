from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView

from .models import Expense, Income, ExpenseCategory
from .forms import ExpenseForm, IncomeForm, ExpenseCategoryForm


class ExpenseListView(LoginRequiredMixin, ListView):
    model = Expense
    template_name = "expenses/expense_list.html"
    paginate_by = 25
    context_object_name = "expenses"

    def get_queryset(self):
        qs = Expense.objects.select_related("category")
        q = self.request.GET.get("q")
        if q:
            qs = qs.filter(expense_number__icontains=q) | qs.filter(reference__icontains=q)
        return qs.order_by("-id")

    def get_context_data(self, **kw):
        ctx = super().get_context_data(**kw)
        ctx["segment"] = "expenses"
        return ctx


class ExpenseCreateView(LoginRequiredMixin, CreateView):
    model = Expense
    form_class = ExpenseForm
    template_name = "expenses/expense_form.html"
    success_url = reverse_lazy("expenses:expense_list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ExpenseUpdateView(LoginRequiredMixin, UpdateView):
    model = Expense
    form_class = ExpenseForm
    template_name = "expenses/expense_form.html"
    success_url = reverse_lazy("expenses:expense_list")


class IncomeListView(LoginRequiredMixin, ListView):
    model = Income
    template_name = "expenses/income_list.html"
    paginate_by = 25
    context_object_name = "incomes"

    def get_queryset(self):
        return Income.objects.select_related().order_by("-id")

    def get_context_data(self, **kw):
        ctx = super().get_context_data(**kw)
        ctx["segment"] = "expenses"
        return ctx


class IncomeCreateView(LoginRequiredMixin, CreateView):
    model = Income
    form_class = IncomeForm
    template_name = "expenses/income_form.html"
    success_url = reverse_lazy("expenses:income_list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class IncomeUpdateView(LoginRequiredMixin, UpdateView):
    model = Income
    form_class = IncomeForm
    template_name = "expenses/income_form.html"
    success_url = reverse_lazy("expenses:income_list")


class ExpenseCategoryListView(LoginRequiredMixin, ListView):
    model = ExpenseCategory
    template_name = "expenses/category_list.html"
    context_object_name = "categories"

    def get_context_data(self, **kw):
        ctx = super().get_context_data(**kw)
        ctx["segment"] = "expenses"
        return ctx


class ExpenseCategoryCreateView(LoginRequiredMixin, CreateView):
    model = ExpenseCategory
    form_class = ExpenseCategoryForm
    template_name = "expenses/category_form.html"
    success_url = reverse_lazy("expenses:category_list")
