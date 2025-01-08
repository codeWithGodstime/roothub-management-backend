from django.contrib import admin
from .models import Announcement


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'receiver_group', 'schedule_date', 'schedule_time', 'created_at')
    list_filter = ('receiver_group', 'schedule_date')
    search_fields = ('title', 'message')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('title', 'message', 'receiver_group')
        }),
        ('Schedule Details', {
            'fields': ('schedule_date', 'schedule_time')
        }),
        ('Important Dates', {
            'fields': ('created_at', 'updated_at')
        }),
    )