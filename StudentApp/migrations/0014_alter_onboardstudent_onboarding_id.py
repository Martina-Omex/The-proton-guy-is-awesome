# Generated by Django 4.2.6 on 2023-12-14 15:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('StudentApp', '0013_alter_onboardstudent_onboarding_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='onboardstudent',
            name='onboarding_id',
            field=models.CharField(default='c10eb210-6187-41a9-8d55-fbf2b31fbdc0', max_length=225),
        ),
    ]