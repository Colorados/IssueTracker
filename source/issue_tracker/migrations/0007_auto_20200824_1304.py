# Generated by Django 2.2 on 2020-08-24 13:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('issue_tracker', '0006_auto_20200824_1121'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='issues',
            name='types_old',
        ),
        migrations.DeleteModel(
            name='IssueType',
        ),
    ]