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
        # /auth/signup/{{id}}/
        context = {
            "url": f"http://127.0.0.1:8000/auth/signup/{instance.onboarding_id}/"
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
