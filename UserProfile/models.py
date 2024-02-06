from django.db import models
from django.contrib.auth.models import User
    
class AdvisorProfile(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def get_department(self):
        from SummerApp.models import Department

        return Department.objects.get(advisor=self)

    def __str__(self):
        return str(self.user)
    
class OnboardAdvisor(models.Model):

    email = models.CharField(max_length=225)

    def __str__(self) -> str:
        return self.email