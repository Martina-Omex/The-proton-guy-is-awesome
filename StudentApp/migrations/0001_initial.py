# Generated by Django 4.2.6 on 2023-11-30 11:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('department', models.CharField(max_length=225)),
                ('academic_year', models.CharField(max_length=225)),
                ('eligibility_letter', models.BooleanField(default=False)),
                ('date_of_letter_approval', models.CharField(blank=True, max_length=225, null=True)),
                ('approved_by', models.CharField(blank=True, max_length=225, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
