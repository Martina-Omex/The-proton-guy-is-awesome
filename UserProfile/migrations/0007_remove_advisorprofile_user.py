# Generated by Django 4.2.6 on 2023-11-30 11:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('UserProfile', '0006_delete_studentprofile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='advisorprofile',
            name='user',
        ),
    ]
