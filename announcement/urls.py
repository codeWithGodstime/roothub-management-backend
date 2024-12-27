from django.urls import path
from rest_framework import routers

from .views import AnnouncementViewset

router = routers.DefaultRouter()
router.register("announcements", AnnouncementViewset, basename="announcements")

urlpatterns = router.urls