# Generated by Django 5.2 on 2025-05-05 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0006_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='reminder_time',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Erinnerungszeit'),
        ),
    ]
