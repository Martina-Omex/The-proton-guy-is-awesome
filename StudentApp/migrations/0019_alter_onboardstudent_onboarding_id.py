# Generated by Django 4.2.6 on 2023-12-16 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('StudentApp', '0018_alter_onboardstudent_onboarding_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='onboardstudent',
            name='onboarding_id',
            field=models.CharField(default='c238a6a9-b860-47fc-885e-cfeda9b50257', max_length=225),
        ),
    ]
