from django.contrib import admin
from .models import Course, CourseSession, StudentCourse


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'program__name', 'instructor__user', 'duration', 'level', 'created_at')
    list_filter = ('program', 'duration', 'level')
    search_fields = ('name', 'program__name', 'instructor__user__fullname')
    ordering = ('-created_at',)
    autocomplete_fields = ('instructor', 'program')
    fieldsets = (
        (None, {
            'fields': ('name', 'program', 'instructor')
        }),
        ('Details', {
            'fields': ('duration', 'level')
        }),
        ('Important Dates', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(CourseSession)
class CourseSessionAdmin(admin.ModelAdmin):
    list_display = ('course', 'start_date', 'estimated_end_date', 'end_date', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('course__name',)
    ordering = ('-start_date',)
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('course', 'is_active')
        }),
        ('Dates', {
            'fields': ('start_date', 'estimated_end_date', 'end_date')
        }),
        ('Important Dates', {
            'fields': ('created_at', 'updated_at')
        }),
    )

@admin.register(StudentCourse)
class StudentCourseAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'created_at')
    search_fields = ('student__user__fullname', 'course__name')
    autocomplete_fields = ('student', 'course')
    ordering = ('-created_at',)

# @admin.register(StudentCourseSession)
# class StudentCourseSessionAdmin(admin.ModelAdmin):
#     list_display = ('student_course', 'course_session', 'created_at')
#     search_fields = (
#         'student_course__student__user__fullname', 
#         'student_course__course__name',
#         'course_session__course__name'
#     )
#     autocomplete_fields = ('student_course', 'course_session')
#     ordering = ('-created_at',)
