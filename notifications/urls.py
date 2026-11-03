from django.urls import path
from . import views

app_name = "notifications"

urlpatterns = [
    path("", views.NotificationListView.as_view(), name="notification_list"),
    path("generate/", views.NotificationGenerateView.as_view(), name="notification_generate"),
    path("<int:pk>/read/", views.NotificationMarkReadView.as_view(), name="notification_read"),
    path("read-all/", views.NotificationMarkAllReadView.as_view(), name="notification_read_all"),
]
