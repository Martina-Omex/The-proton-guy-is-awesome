from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from SummerApp.models import Department
from UserProfile.models import *
from StudentApp.models import StudentProfile,OnboardStudent
from django.contrib import messages
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate,login, logout
from django.contrib import messages

get_all_departments = Department.objects.all()

def Login(request):

    if request.user.is_authenticated:
        return redirect('homepage')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        authenticate_user = authenticate(username=username, password=password)
        if authenticate_user is not None:
            login(request, authenticate_user)
            return redirect('homepage')
        else:
            messages.error(request, "Invalid login credentials")
            return redirect('login')
    
    return render(request, 'login.html')

def Logout(request):

    logout(request)
    return redirect('login')

def Signup(request, _id):

    if request.user.is_authenticated:
        return redirect('homepage')

    onboard_student_object = None

    try:
        onboard_student_object = OnboardStudent.objects.get(onboarding_id=_id)
    except OnboardStudent.DoesNotExist:
        messages.error(request, "You are not a valid student applicant!")
        return redirect('signup')

    # if user submits form
    if request.method == "POST":

        # grabbing user input from form 
        first_name = request.POST.get('fname')
        last_name = request.POST.get('lname')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect('signup')

        # creating a new user object 
        create_new_user = User.objects.create_user(
            first_name = first_name,
            last_name = last_name,
            username = onboard_student_object.student_number,
            email = onboard_student_object.email,
            password = password,
        )
        create_new_user.save()

        create_new_profile = StudentProfile(
            user = create_new_user,
            student_number = onboard_student_object.student_number,
            department = onboard_student_object.department,
            academic_year = onboard_student_object.academic_year,
            approved_by = onboard_student_object.approved_by
        )

        create_new_profile.save()

        messages.success(request, "Account created successfully! Proceed to login")
        return redirect('login')

        # work on rediorect to homw page

    context = {
        "departments": get_all_departments,
        "student": onboard_student_object
    }

    return render(request, 'signup.html', context)

def create_advisor(request):

    if request.method == "POST":

        print(request.POST)

        # grabbing user input from form 
        first_name = request.POST.get('fname')
        last_name = request.POST.get('lname')
        username = request.POST.get('username')
        email = request.POST.get('email')
        # department = request.POST.get('department')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect('create-advisor')

        if not OnboardAdvisor.objects.filter(email=email).exists():
            messages.error(request, "You are not a valid advisor applicant!")
            return redirect('create-advisor')

        # creating a new user object 
        create_new_user = User.objects.create_user(
            first_name = first_name,
            last_name = last_name,
            username = username,
            password = password,
            is_staff = True,
            email=email
        )
        create_new_user.save()

        advisor_group = Group.objects.get(name='Advisor')
        create_new_user.groups.add(advisor_group)

        create_new_profile = AdvisorProfile(
            user = create_new_user,
        )
        create_new_profile.save()
        messages.success(request, "Your advisor profile has been created successfully!")
        return redirect('create-advisor')

    context = {
        "departments": get_all_departments
    }

    return render(request, 'create_advisor.html', context)