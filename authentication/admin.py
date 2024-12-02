from django.contrib import admin

# Register your models here.
from .models import User, Program


admin.site.register([User, Program])