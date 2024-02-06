from django.db import models
from UserProfile.models import AdvisorProfile

class Department(models.Model):

    name = models.CharField(max_length=225)
    advisor = models.ForeignKey(AdvisorProfile, on_delete=models.DO_NOTHING, null=True, blank=True)

    def __str__(self):
        return self.name