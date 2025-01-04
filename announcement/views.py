import logging
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema_field, extend_schema, extend_schema_view, OpenApiParameter
from django.db import transaction

from .serializers import AnnouncementSerializer
from .models import Announcement
from .tasks import send_announcement_email

logger = logging.getLogger(__name__)

class CustomIsAdminUser(permissions.IsAdminUser):
    """
    Allows access only to admin users.
    """

    def has_permission(self, request, view):
        return bool(request.user.is_superuser)


@extend_schema_view(tags=["Announcements"])
class AnnouncementViewset(viewsets.ModelViewSet):
    serializer_class = AnnouncementSerializer.AnnouncementRetrieveSerializer
    queryset = Announcement.objects.all()
    permission_classes = [CustomIsAdminUser]

    @extend_schema(
        request=AnnouncementSerializer.AnnouncementCreateSerializer
    )
    @transaction.atomic()
    def create(self, request, *args, **kwargs):
        logger.info(f"Create announcement initiated by user: {request.user}")
        logger.debug(f"Request data: {request.data}")
        
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            logger.info("Announcement data validated successfully.")
        except Exception as e:
            logger.error(f"Validation failed: {e}")
            raise

        announcement = serializer.save()
        logger.info(f"Announcement created with ID: {announcement.id}")

        # Check if schedule is provided; if not, send immediately
        if not announcement.schedule_date or not announcement.schedule_time:
            logger.info("No schedule date/time provided. Sending email immediately.")
            try:
                send_announcement_email(announcement.id)
                logger.info(f"Email sent for announcement ID: {announcement.id}")
            except Exception as e:
                logger.error(f"Failed to send email for announcement ID {announcement.id}: {e}")
        
        announcement.save()
        logger.debug(f"Announcement saved to database: {announcement}")

        headers = self.get_success_headers(serializer.data)
        logger.info("Create announcement process completed successfully.")
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)