from django.db import models
from django.contrib.auth.models import User
import datetime
import uuid
from SummerApp.models import Department
from UserProfile.models import AdvisorProfile

current_year = datetime.datetime.now().year
# Calculate the previous year
previous_year = current_year - 1

ACADEMIC_YEAR_CHOICES = [
    (f"SPRING {previous_year}-{current_year}", f"SPRING {previous_year}-{current_year}"),   
    (f"SUMMMER {previous_year}-{current_year}", f"SUMMER {previous_year}-{current_year}"),
    (f"FALL {previous_year}-{current_year}", f"FALL {previous_year}-{current_year}"),
]

INTERNSHIP_REPORT_STATUS_CHOICES = [
    ("Accepted", "Accepted"),
    ("Rejected", "Rejected"),
    ("Correction", "Correction")
]

class OnboardStudent(models.Model):

    onboarding_id = models.CharField(max_length=225, default=f"{uuid.uuid4()}")
    student_number = models.CharField(max_length=225, null=True, blank=True)
    department = models.ForeignKey(Department, null=True, blank=True, on_delete=models.CASCADE)
    academic_year = models.CharField(max_length=225, choices=ACADEMIC_YEAR_CHOICES)
    email = models.EmailField(null=True, blank=True)
    eligibility_letter = models.BooleanField(default=True)
    date_of_letter_approval = models.DateField(null=True, blank=True)
    approved_by = models.ForeignKey(AdvisorProfile, on_delete=models.CASCADE, null=True, blank=True)

class StudentProfile(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    student_number = models.CharField(max_length=225, null=True, blank=True)
    department = models.ForeignKey(Department, related_name="Student_department", null=True, blank=True, on_delete=models.CASCADE)
    academic_year = models.CharField(max_length=225, choices=ACADEMIC_YEAR_CHOICES)
    eligibility_letter = models.BooleanField(default=True)
    date_of_letter_approval = models.DateField(null=True, blank=True)
    approved_by = models.ForeignKey(AdvisorProfile, related_name="appreoved_by_who", on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return str(self.user)
    
    def get_student_documentation(self):

        return StudentDocumentation.objects.get(student=self)
    
    def get_student_company_application(self):

        from CompanyApplication.models import Application

        return Application.objects.filter(student=self).order_by('-date_of_application')
    
class StudentDocumentation(models.Model):

    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    logbook_signature_date = models.DateField()
    internship_report_submit_date = models.DateField()
    internship_report_status = models.CharField(max_length=225, choices=INTERNSHIP_REPORT_STATUS_CHOICES)
    oral_exam_date = models.DateField()
    oral_exam_status = models.CharField(max_length=225)
    remark_notices = models.TextField()

    def __str__(self):
        return self.student.user.username