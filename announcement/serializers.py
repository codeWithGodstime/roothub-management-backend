from rest_framework import serializers
from .models import Announcement


class AnnouncementSerializer:

    class AnnouncementCreateSerializer(serializers.ModelSerializer):
        class Meta:
            model = Announcement
            fields = [
                "title",
                "message",
                "schedule_date",
                "schedule_time",
                "receiver_group"
            ]

    class AnnouncementRetrieveSerializer(serializers.ModelSerializer):
        class Meta:
            model = Announcement
            fields = [
                "id",
                "title",
                "message",
                "schedule_date",
                "schedule_time",
                "receiver_group",
                "created_at",
                "updated_at"
            ]