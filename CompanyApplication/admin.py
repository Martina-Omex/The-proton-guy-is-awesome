from django.contrib import admin
from .models import *
from CompanyApplication.models import Application
from SummerApp.models import Department
from UserProfile.models import AdvisorProfile

class ApplicationAdmin(admin.ModelAdmin):
    search_fields = ['student__studentprofile__student_number']
    list_display = ['student', 'company_name', 'country', 'application_status', 'is_selected']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            try:
                advisor_profile = AdvisorProfile.objects.get(user=request.user)
                department = Department.objects.get(advisor=advisor_profile)
                return qs.filter(student__department=department)
            except AdvisorProfile.DoesNotExist:
                return qs.none()
        
        else:
            return qs

admin.site.register(Application, ApplicationAdmin)