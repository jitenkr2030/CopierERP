from django.urls import path
from . import views

app_name = "expenses"

urlpatterns = [
    path("", views.ExpenseListView.as_view(), name="expense_list"),
    path("new/", views.ExpenseCreateView.as_view(), name="expense_create"),
    path("<int:pk>/edit/", views.ExpenseUpdateView.as_view(), name="expense_edit"),
    path("incomes/", views.IncomeListView.as_view(), name="income_list"),
    path("incomes/new/", views.IncomeCreateView.as_view(), name="income_create"),
    path("incomes/<int:pk>/edit/", views.IncomeUpdateView.as_view(), name="income_edit"),
    path("categories/", views.ExpenseCategoryListView.as_view(), name="category_list"),
    path("categories/new/", views.ExpenseCategoryCreateView.as_view(), name="category_create"),
]
