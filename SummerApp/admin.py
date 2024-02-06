from django.contrib import admin
from .models import *

class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'advisor']

admin.site.register(Department, DepartmentAdmin)