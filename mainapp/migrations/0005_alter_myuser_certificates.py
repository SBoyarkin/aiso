# Generated by Django 5.1.2 on 2024-11-22 05:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0004_remove_certificate_owner_myuser_certificates'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='certificates',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='owner', to='mainapp.certificate'),
        ),
    ]
