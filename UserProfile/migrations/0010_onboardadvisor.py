# Generated by Django 4.2.6 on 2023-12-14 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserProfile', '0009_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OnboardAdvisor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=225)),
            ],
        ),
    ]
