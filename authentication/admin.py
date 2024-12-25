from django.contrib import admin

# Register your models here.
from .models import User, Program, Instructor, InstructorSkill, Student, StudentPayment


admin.site.register([User, Program, Instructor, InstructorSkill, Student, StudentPayment])