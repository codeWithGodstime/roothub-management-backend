from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema_field, extend_schema, extend_schema_view, OpenApiParameter
from django.db import transaction

from .serializers import AnnouncementSerializer
from .models import Announcement
from .tasks import send_announcement_email


class CustomIsAdminUser(permissions.IsAdminUser):
    """
    Allows access only to admin users.
    """

    def has_permission(self, request, view):
        return bool(request.user.is_superuser)


@extend_schema_view(tag=["Announcements"])
class AnnouncementViewset(viewsets.ModelViewSet):
    serializer_class = AnnouncementSerializer.AnnouncementRetrieveSerializer
    queryset = Announcement.objects.all()
    permission_classes = [CustomIsAdminUser]

    @extend_schema(
            request=AnnouncementSerializer.AnnouncementCreateSerializer
    )
    @transaction.atomic()
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        announcement = serializer.save()
        
        # Check if schedule is provided; if not, send immediately
        if not announcement.schedule_date or not announcement.schedule_time:
            send_announcement_email(announcement.id)
            announcement.sent = True
            announcement.save()
        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
