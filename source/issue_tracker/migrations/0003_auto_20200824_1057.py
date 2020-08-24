# Generated by Django 2.2 on 2020-08-24 10:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('issue_tracker', '0002_auto_20200816_1715'),
    ]

    operations = [
        migrations.CreateModel(
            name='IssueType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('issue', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='issue_types', to='issue_tracker.Issues', verbose_name='Задача')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='type_issues', to='issue_tracker.Type', verbose_name='Типы')),
            ],
        ),
        migrations.AddField(
            model_name='issues',
            name='types',
            field=models.ManyToManyField(blank=True, related_name='issues', through='issue_tracker.IssueType', to='issue_tracker.Type'),
        ),
    ]