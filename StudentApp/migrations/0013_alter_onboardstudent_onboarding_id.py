# Generated by Django 4.2.6 on 2023-12-14 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('StudentApp', '0012_remove_studentprofile_department_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='onboardstudent',
            name='onboarding_id',
            field=models.CharField(default='c86283ac-cee3-4413-b910-b48b5a500ab8', max_length=225),
        ),
    ]
