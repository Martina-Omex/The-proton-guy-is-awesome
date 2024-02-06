from django.contrib import admin
from .models import *
from UserProfile.models import AdvisorProfile
from SummerApp.models import Department
from django import forms
from django.contrib.auth.models import Group

class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = '__all__'

class OnboardStudentAdmin(admin.ModelAdmin):
    list_display = ['approved_by', 'student_number', 'department', 'academic_year', 'email', 'eligibility_letter', 'date_of_letter_approval']
    editable_fields = ('user', 'student_number', 'academic_year', 'eligibility_letter', 'date_of_letter_approval', 'email')

    form = StudentProfileForm

    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)

        if request.user.is_superuser:
            # If the current user is a superuser, show all fields
            return fields
        else:
            # Otherwise, exclude the 'user' field
            return [field for field in fields if field != 'user']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not request.user.is_superuser and db_field.name == 'user':
            # If the user is not a superuser and the field is 'user', filter by the "Student" group
            student_group = Group.objects.get(name='Student')
            kwargs['queryset'] = student_group.user_set.all()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_readonly_fields(self, request, obj=None):
        # Make all fields readonly by default
        readonly_fields = set([field.name for field in self.model._meta.fields])

        # Make editable_fields writable
        readonly_fields -= set(self.editable_fields)

        # Allow superusers to edit all fields
        if request.user.is_superuser:
            return []

        return list(readonly_fields)

    def save_model(self, request, obj, form, change):
        # Set the user field to the currently logged-in user
        if not request.user.is_superuser:
            advisor = AdvisorProfile.objects.get(user=request.user)
            obj.approved_by = advisor
            obj.department = advisor.get_department()
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        advisor = AdvisorProfile.objects.get(user=request.user)
        if not request.user.is_superuser:
            try:
                advisor_profile = advisor
                department = Department.objects.get(advisor=advisor_profile)
                return qs.filter(department=department)
            except AdvisorProfile.DoesNotExist:
                return qs.none()
        
        else:
            return qs

admin.site.register(OnboardStudent,OnboardStudentAdmin)

class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'student_number', 'department', 'academic_year', 'eligibility_letter', 'date_of_letter_approval', 'approved_by')
    editable_fields = ('user', 'student_number', 'academic_year', 'eligibility_letter', 'date_of_letter_approval', 'email')

    form = StudentProfileForm

    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)

        if request.user.is_superuser:
            # If the current user is a superuser, show all fields
            return fields
        else:
            # Otherwise, exclude the 'user' field
            return [field for field in fields if field != 'user']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not request.user.is_superuser and db_field.name == 'user':
            # If the user is not a superuser and the field is 'user', filter by the "Student" group
            student_group = Group.objects.get(name='Student')
            kwargs['queryset'] = student_group.user_set.all()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_readonly_fields(self, request, obj=None):
        # Make all fields readonly by default
        readonly_fields = set([field.name for field in self.model._meta.fields])

        # Make editable_fields writable
        readonly_fields -= set(self.editable_fields)

        # Allow superusers to edit all fields
        if request.user.is_superuser:
            return []

        return list(readonly_fields)

    def save_model(self, request, obj, form, change):
        # Set the user field to the currently logged-in user
        if not request.user.is_superuser:
            advisor = AdvisorProfile.objects.get(user=request.user)
            obj.approved_by = advisor
            obj.department = advisor.get_department()
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        advisor = AdvisorProfile.objects.get(user=request.user)
        if not request.user.is_superuser:
            try:
                advisor_profile = advisor
                department = Department.objects.get(advisor=advisor_profile)
                return qs.filter(department=department)
            except AdvisorProfile.DoesNotExist:
                return qs.none()
        
        else:
            return qs
   

admin.site.register(StudentProfile, StudentProfileAdmin)

class StudentDocAdmin(admin.ModelAdmin):
    list_display = ['student', 'logbook_signature_date', 'internship_report_submit_date', 'internship_report_status', 'oral_exam_date', 'oral_exam_status']

    # form = StudentProfileForm

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

admin.site.register(StudentDocumentation, StudentDocAdmin)
