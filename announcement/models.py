from django.db import models
from utils.model_mixins import BaseModelMixin


class Announcement(BaseModelMixin):
    RECEIVER_GROUP = (
        ("ALL", "All"),
        ("TRAINER", "Trainer"),
        ("TRAINEE", "Trainee"),
    )
    title = models.CharField(max_length=200, unique=True)
    message = models.TextField()
    schedule_date = models.DateField(null=True, blank=True)
    schedule_time = models.TimeField(null=True, blank=True)
    receiver_group = models.CharField(max_length=30, choices=RECEIVER_GROUP, default="ALL")