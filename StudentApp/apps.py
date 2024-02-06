from django.apps import AppConfig


class StudentappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'StudentApp'

    def ready(self):
        import StudentApp.signals  # Replace 'your_app' with the actual name of your app