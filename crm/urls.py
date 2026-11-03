from django.urls import path
from . import views

app_name = "crm"

urlpatterns = [
    path("", views.CallListView.as_view(), name="call_list"),
    path("new/", views.CallCreateView.as_view(), name="call_create"),
    path("<int:pk>/", views.CallDetailView.as_view(), name="call_detail"),
    path("<int:pk>/edit/", views.CallUpdateView.as_view(), name="call_edit"),
    path("<int:pk>/followups/", views.AddFollowUpView.as_view(), name="call_followup_add"),
]
