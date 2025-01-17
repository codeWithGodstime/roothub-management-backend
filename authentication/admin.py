from django.contrib import admin

# Register your models here.
from .models import User, Program, Instructor, InstructorSkill, Student, StudentPayment, Student, Skill

from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'fullname', 'is_instructor', 'is_student', 'is_active', 'created_at')
    list_filter = ('is_instructor', 'is_student', 'is_active', 'is_superuser', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name', 'next_of_kin_name', 'next_of_kin_email')
    ordering = ('-created_at',)
    readonly_fields = ('last_login', 'created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('email', 'password', 'first_name', 'last_name', 'home_address')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Next of Kin', {
            'fields': ('next_of_kin_name', 'next_of_kin_relationship', 'next_of_kin_contact', 'next_of_kin_email')
        }),
        ('Important dates', {
            'fields': ('last_login', 'created_at', 'updated_at')
        }),
    )

@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ('name', 'duration', 'total_amount', 'created_at')
    list_filter = ('duration',)
    search_fields = ('name',)
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ('user', 'account_name', 'bank_name', 'created_at')
    search_fields = ('user__email', 'account_name', 'bank_name')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'type', 'payment_plan', 'program__name', 'session', 'created_at')
    list_filter = ('type', 'payment_plan', 'program', 'session')
    search_fields = ('user__email', 'program__name')
    ordering = ('-created_at',)

@admin.register(StudentPayment)
class StudentPaymentAdmin(admin.ModelAdmin):
    list_display = ('student', 'amount', 'payment_date', 'created_at')
    list_filter = ('payment_date',)
    search_fields = ('student__user__email',)
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')

@admin.register(InstructorSkill)
class InstructorSkillAdmin(admin.ModelAdmin):
    # list_display = []
    ...

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    # list_display = []
    ...
