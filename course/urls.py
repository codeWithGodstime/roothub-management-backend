from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import CourseViewset

router = DefaultRouter()
router.register("courses", CourseViewset, basename="courses")

urlpatterns = router.urls