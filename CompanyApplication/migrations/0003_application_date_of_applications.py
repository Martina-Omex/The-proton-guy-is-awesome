# Generated by Django 4.2.6 on 2023-12-16 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CompanyApplication', '0002_alter_application_country'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='date_of_applications',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
