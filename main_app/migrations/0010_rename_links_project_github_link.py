# Generated by Django 4.2.1 on 2023-06-09 01:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0009_remove_project_journals_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='project',
            old_name='links',
            new_name='github_link',
        ),
    ]
