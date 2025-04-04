# Generated by Django 5.1.2 on 2024-11-22 06:30

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0005_alter_myuser_certificates'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='myuser',
            name='certificates',
        ),
        migrations.AddField(
            model_name='certificate',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='certificates', to=settings.AUTH_USER_MODEL),
        ),
    ]
