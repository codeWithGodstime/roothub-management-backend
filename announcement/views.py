from rest_framework import viewsets, permissions


from .serializers import AnnouncementSerializer
from .models import Announcement


class CustomIsAdminUser(permissions.IsAdminUser):
    """
    Allows access only to admin users.
    """

    def has_permission(self, request, view):
        return bool(request.user.is_superuser)


class AnnouncementViewset(viewsets.ModelViewSet):
    serializer_class = AnnouncementSerializer.AnnouncementRetrieveSerializer
    queryset = Announcement.objects.all()
    permission_classes = [CustomIsAdminUser]
