# Generated by Django 5.1.2 on 2024-12-09 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0007_myuser_middle_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='organization',
            name='user',
        ),
        migrations.AddField(
            model_name='myuser',
            name='organization',
            field=models.ManyToManyField(blank=True, related_name='user', to='mainapp.organization'),
        ),
    ]
