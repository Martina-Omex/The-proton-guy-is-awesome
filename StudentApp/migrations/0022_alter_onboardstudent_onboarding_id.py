# Generated by Django 4.2.6 on 2023-12-18 16:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('StudentApp', '0021_alter_onboardstudent_onboarding_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='onboardstudent',
            name='onboarding_id',
            field=models.CharField(default='204efd62-ccee-40aa-b9be-51b301994f1d', max_length=225),
        ),
    ]
