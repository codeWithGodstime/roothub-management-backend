from django.contrib import admin
from .models import Course, CourseSession, StudentCourse


admin.site.register([Course, CourseSession, StudentCourse])