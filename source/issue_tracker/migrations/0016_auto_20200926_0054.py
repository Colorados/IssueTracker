# Generated by Django 2.2 on 2020-09-26 00:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('issue_tracker', '0015_issues_project'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issues',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='projects', to='issue_tracker.Project', verbose_name='Проект'),
        ),
    ]
