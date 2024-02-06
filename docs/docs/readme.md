# Summer Project documentation
================================================================
1. Tech stack:
    -   Backend: Python & Django 
    -   Frontend: HTML, CSS & Vanilla Javacsript
    -   Database: sqlite3
    -   Media storage: Cloudinary
----------------------------------------------------------------

## Installing & Runnning
Note: It is possible to run this on Windows, mac, and linux but python has to be installed on machine to run the project
2. Running the project:
     &nbsp;
    - Open terminal and navigate to where project is
    &nbsp;
    - Create/activte virtual environment by the following command:
        &nbsp;
        - First make sure `pipenv` is installed: 
        `pip install pipenv` or `pip3 install pipenv`
        &nbsp;
        - Create or activate virtual environment by running: 
        `pipenv shell` 
        &nbsp;
        in the base directory which is `summer-training`
    &nbsp;
    - Install the required libraries to run project from requirments.txt file by running the following command: 
    &nbsp;
    `pip install -r requirements.txt` or 
    `pip3 install -r requirements.txt`
    &nbsp;
    - Navigate to the `SummerPrj` folder in the terminal after installing the requirements
    

- Run the local development server:
&nbsp;
    `python manage.py runserver` or 
    `python3 manage.py runserver`

----------------------------------------------------------------

## Program Flow & Usage
================================================================

### Admin actions

1. Creating an admin(superuser):
&nbsp;
    - Break out of the terminal and run: 
        `python manage.py createsuperuser` or
        `python3 manage.py createsuperuser`
        &nbsp;
        You will be prompted to enter details about the user. After this, an admin that can manage all operations on the website will be created
&nbsp;
2. An admin onboarding an advisor to be created:
    &nbsp;
    - Log into the admin dashboard here: 
    http://127.0.0.1:8000/admin with 
    the admin user details you had just created
    &nbsp;
    - Scrolldown to unboard advisors and click it. 
    &nbsp;
    - Click 'Add Onboard Advisor', and type in the email of the advisor you want to unboard; Note, This prevents any user from just signing up on the platform because when a user wants to sign up as an advisor, they will have to provide an email address, and if that email they have provided exists under the OnboardAdvisors table, their account will be created, else an error will be displayed telling them they are not a valid user that can signup as an advisor. Below is the code that represents the database table for onboarding an advisor in the file: 
    &nbsp;
    `UserProfile/models.py`
        &nbsp;
        ```python
        class OnboardAdvisor(models.Model):
            email = models.CharField(max_length=225)

            def __str__(self) -> str:
                return self.email
        ```
    &nbsp;
    - The next part is done by the user who is being signed up as an advisor. They have to go to the url: 
        http://127.0.0.1:8000/auth/create-advisor
        where they will need to fill out details like first name, last name, email... After which a verification will be done to see if they are an eligible user for signing up as an advisor. 
        Below is the code that creates an advisor in the file:
        &nbsp;
        `AuthenticationApp/views.py`
        &nbsp;
        ```python
        from django.shortcuts import render, redirect
        from django.contrib.auth.models import User
        from UserProfile.models import *
        from StudentApp.models import OnboardStudent
        from django.contrib import messages
        from django.contrib.auth.models import Group

        def create_advisor(request):
            
            # check if user submitted form
            if request.method == "POST":

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
                return redirect('admin')

            context = {
                "departments": get_all_departments
            }

            return render(request, 'create_advisor.html', context)
        ```
    &nbsp;
    - Their account will then be created and they can proceed to login to the admin page here: 
        http://127.0.0.1:8000/admin/ 
    &nbsp;
    The code below represents database table for users
    &nbsp;
        ```python
        class User(AbstractBaseUser, PermissionsMixin):
            email = models.EmailField(unique=True)
            username = models.CharField(max_length=30, unique=True)
            first_name = models.CharField(max_length=30, blank=True)
            last_name = models.CharField(max_length=30, blank=True)
            is_active = models.BooleanField(default=True)
            is_staff = models.BooleanField(default=False)

            objects = UserManager()

            USERNAME_FIELD = 'email'
            REQUIRED_FIELDS = ['username']

        ```
    &nbsp;
    
3. An admin adding a department & Assigning an advisor:

    - Scroll down to Department under SummerApp and click it
    &nbsp;
    - Click Add department and type the department name. Also specify the department advisor but it can be left blank also if advisor does not exist yet. The advisor can be set later.
    &nbsp;
    - Click save
    Below is the code that represents the database table for Departments in file:
    &nbsp;
    `SummerApp/models.py`
    &nbsp;
   ```python
    from django.db import models
    from UserProfile.models import AdvisorProfile

    class Department(models.Model):
        name = models.CharField(max_length=225)
        advisor = models.ForeignKey(AdvisorProfile, on_delete=models.DO_NOTHING, null=True, blank=True)

        def __str__(self):
            return self.name
    ``` 
----------------------------------------------------------------
### Advisor actions

1. Advisors onboarding Students:

    - Sign in as advisor
    &nbsp;
    - Click 'Onboard students' under StudentAPP in the admin dashboard and click add onboard student
    &nbsp;
    - Fill out the details in the formand click submit. After you submit, an email containing a signup link will be sent to the student's email which you had just filled, telling them to continue the signup process. After which the students will be taken to the following url after clicking the link:
    http://127.0.0.1:800/signup/<str:_id>/
    where str_id is the onboarding id. 
    &nbsp;
    If this id does not exist in the database, it means this is an invalid request and will display an error message telling the user that they are not eligible to signup as a student.
    Note that when an advisor creates a new student, the student's department get's set automatically to the advisor's department.
    Below is the code representing the database table for onboarding a student in file:
        &nbsp;
        `StudentApp/models.py`
        &nbsp;

        ```python
        from django.db import models
        import uuid

        class OnboardStudent(models.Model):

            onboarding_id = models.CharField(max_length=225, default=f"{uuid.uuid4()}")
            student_number = models.CharField(max_length=225, null=True, blank=True)
            department = models.ForeignKey(Department, null=True, blank=True, on_delete=models.CASCADE)
            academic_year = models.CharField(max_length=225, choices=ACADEMIC_YEAR_CHOICES)
            email = models.EmailField(null=True, blank=True)
            eligibility_letter = models.BooleanField(default=True)
            date_of_letter_approval = models.DateField(null=True, blank=True)
            approved_by = models.ForeignKey(AdvisorProfile, on_delete=models.CASCADE, null=True, blank=True)
        ```
    &nbsp;
    - Below is the code that sends the email to the student. It is a signal that listens for when a new object of the OnboardStudent is created:
        &nbsp;
        `StudentApp/signals.py`
        &nbsp;

        ```python
        from django.db.models.signals import post_save
        from django.dispatch import receiver
        from django.core.mail import EmailMessage
        from django.conf import settings
        from .models import *
        from django.template.loader import render_to_string

        @receiver(post_save, sender=OnboardStudent)  # Replace 'User' with your model
        def send_email_on_creation(sender, instance, created, **kwargs):
            if created:
                # Assuming 'email' is a field in your model containing the recipient's email
                recipient_email = instance.email

                # Customize the subject and message as per your requirements
                subject = 'Create Account: Summer internship'
                # message = f'<p>You can now create your account using this <a href="127.0.0.1:8000/auth/signup/{instance.onboarding_id}">Link</a></p>'
                email_template_name = 'email.html'

                context = {
                    "id": instance.onboarding_id
                }
                email_body = render_to_string(email_template_name, context)     

                email_mess = EmailMessage (
                    subject,
                    email_body, # email content
                    settings.EMAIL_HOST_USER, # email sender
                    [recipient_email] # recipients
                )
                email_mess.fail_silently = True
                email_mess.content_subtype = 'html'
                email_mess.send()

        ```
    - After the student fills the form and submits, a student profile get's created for them and the data from the onboard student class is then copied to a new student profile class and saved. Below ius the database table that represents student profiles:

        &nbsp;
            `StudentApp/models.py`

        &nbsp;
        ```python
        from django.contrib.auth.models import User
        from SummerApp.models import Department
        from UserProfile.models import AdvisorProfile

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
        ```
    
    &nbsp;
    - They will then be redirected to the login page, where they can login with theor details. After login, they will be redirected to the home page, where they can see their internship applications. 
&nbsp;
2. Advisors creating applications for students:
    &nbsp;
    - Head to the admin dashboard and click Applications under Companyapplication and click add application
    &nbsp;
    - Fill out the application form and click save. After saving, the student will be able to see this application displayed when they login to the portal. The status of the application can be edited anytime an update comes. Below is the code & database table that represents an application to a company application:
    
        &nbsp;
            `CompanyApplication/models.py`
        &nbsp;

        ```python
        from django.db import models
        from StudentApp.models import StudentProfile

        COUNTRY_CHOICES = [
            ('Afghanistan', 'Afghanistan'),
            ('Albania', 'Albania'),
            ...
        ]

        class Application(models.Model):
            student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
            company_name = models.CharField(max_length=225)
            country = models.CharField(max_length=225, choices=COUNTRY_CHOICES)
            application_status = models.BooleanField(default=False)
            is_selected = models.BooleanField(default=False)
            remark = models.TextField(null=True, blank=True)
            company_information_file = models.FileField('company-information/', null=True, blank=True)
            date_of_application = models.DateTimeField(auto_now_add=True, null=True, blank=True)

            def __str__(self):
                return self.student.user.username
        ```
&nbsp;

3. Advisors creating documentations for students:
    &nbsp;
    - Head to the admin dashboard and click Student documentations under Companyapplication and click add student documentation
    &nbsp;
    - Fill the form with the desired details and click save. Also note that all these can be edited and updated anytime by the advisor. Below is the code that represents the database tablr for student documentations:
        
        &nbsp;
            `StudentApp/models.py`

        &nbsp;

        ```python
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
        ```

----------------------------------------------------------------
### Student Actions
Students are only allowed to perform basic operations like login, signup, and viewing their applications to companies. 

- Logging in: 
    The students can login using this link:
    http://127.0.0.1:8000/auth/login/
    &nbsp;
    How the login works:
    &nbsp;
    &nbsp;
    `AuthenticationApp/views.py`

    &nbsp;
    ```python
    # importing needed libraries
    from django.shortcuts import render, redirect
    from django.contrib.auth.models import User
    from django.contrib.auth import authenticate,login,
    from django.contrib import messages

    def Login(request):
    # redirect user to home page if they are logged in
    if request.user.is_authenticated:
        return redirect('homepage')
    
    # checking if user has submitted form
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # authenticate the details 
        authenticate_user = authenticate(username=username, password=password)
        if authenticate_user is not None:
            # log user in if details are correct 
            login(request, authenticate_user)
            return redirect('homepage')
        else:
            # return an error if details are not correct
            messages.error(request, "Invalid login credentials")
            return redirect('login')
    
    return render(request, 'login.html')
    ```
&nbsp;
- Logging out:
    The students can login using this link:
    http://127.0.0.1:8000/auth/logout/
    &nbsp;
    `AuthenticationApp/views.py`

    &nbsp;
    ```python
    def Logout(request):
        # logging out the user and redirecting to login page
        logout(request)
        return redirect('login')
    ```
&nbsp;
- Signing up:
    below is the code for signing up a user
    &nbsp;
    `AuthenticationApp/views.py`

    &nbsp;
    ```python
    def Signup(request, _id):
        # redirect user to home page if they are logged in
        if request.user.is_authenticated:
            return redirect('homepage')

        onboard_student_object = None

        ''' 
        try to see if an onboard student object with the id provided exists in the databaase
        '''
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

            # creating a new student profile and saving
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
    ```

----------------------------------------------------------------

### Visual representation of database tables

![Alt Text](/docs/my_project_visualized.png)
----------------------------------------------------------------