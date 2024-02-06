from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import StudentProfile

@login_required
def homepage(request):

    get_student_profile = StudentProfile.objects.get(user=request.user)

    context = {
        "applications": get_student_profile
    }

    return render(request, 'home.html',context)