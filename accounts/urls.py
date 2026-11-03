from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("", views.UserListView.as_view(), name="user_list"),
    path("new/", views.UserCreateView.as_view(), name="user_create"),
    path("<int:pk>/", views.UserDetailView.as_view(), name="user_detail"),
    path("<int:pk>/edit/", views.UserUpdateView.as_view(), name="user_edit"),
]
