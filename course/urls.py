from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import CourseViewset, CourseSessionViewset

router = DefaultRouter()
router.register("courses", CourseViewset, basename="courses")
router.register("sessions", CourseSessionViewset, basename="sessions")

urlpatterns = router.urls