# Generated by Django 5.0.2 on 2024-03-13 01:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Task_Quest_Config', '0002_task_priority'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='email',
        ),
        migrations.RemoveField(
            model_name='task',
            name='password',
        ),
    ]