# Generated by Django 5.0.1 on 2024-01-03 14:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_remove_project_deals'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dealproject',
            name='deal',
        ),
        migrations.RemoveField(
            model_name='dealproject',
            name='project',
        ),
        migrations.DeleteModel(
            name='Deal',
        ),
        migrations.DeleteModel(
            name='DealProject',
        ),
        migrations.DeleteModel(
            name='Project',
        ),
    ]
