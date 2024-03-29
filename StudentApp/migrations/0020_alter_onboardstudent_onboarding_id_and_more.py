# Generated by Django 4.2.6 on 2023-12-18 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('StudentApp', '0019_alter_onboardstudent_onboarding_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='onboardstudent',
            name='onboarding_id',
            field=models.CharField(default='09c3f2e0-d67d-4c0c-a441-0908ccc868fc', max_length=225),
        ),
        migrations.AlterField(
            model_name='studentprofile',
            name='academic_year',
            field=models.CharField(choices=[('SPRING 2022-2023', 'SPRING 2022-2023'), ('SUMMMER 2022-2023', 'SUMMER 2022-2023'), ('FALL 2022-2023', 'FALL 2022-2023')], max_length=225),
        ),
    ]
