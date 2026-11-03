from django.db import models
from django.conf import settings
from companies.models import Company


class Call(models.Model):
    CALL_STATUS = [
        ("new", "New"),
        ("interested", "Interested"),
        ("requirement_received", "Requirement Received"),
        ("follow_up_pending", "Follow-up Pending"),
        ("completed", "Completed"),
        ("not_interested", "Not Interested"),
    ]
    DIRECTIONS = [
        ("incoming", "Incoming"),
        ("outgoing", "Outgoing"),
    ]

    call_id = models.CharField(max_length=40, unique=True)
    company = models.ForeignKey(Company, on_delete=models.PROTECT, related_name="calls")
    contact_person = models.CharField(max_length=120, blank=True)
    phone = models.CharField(max_length=40)
    call_date = models.DateField()
    call_time = models.TimeField(null=True, blank=True)
    direction = models.CharField(max_length=10, choices=DIRECTIONS, default="outgoing")
    purpose = models.CharField(max_length=120, blank=True)
    notes = models.TextField(blank=True)
    next_follow_up = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=30, choices=CALL_STATUS, default="new")
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                                     null=True, blank=True, related_name="calls_assigned")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                                   null=True, related_name="calls_created")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-call_date", "-id"]

    def __str__(self):
        return f"{self.call_id} - {self.company}"


class FollowUp(models.Model):
    call = models.ForeignKey(Call, on_delete=models.CASCADE, related_name="followups")
    date = models.DateField()
    notes = models.TextField()
    next_follow_up = models.DateField(null=True, blank=True)
    done_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Follow-up for {self.call.call_id} on {self.date}"
