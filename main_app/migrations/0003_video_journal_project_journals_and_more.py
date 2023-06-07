# Generated by Django 4.2.1 on 2023-06-07 18:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_task_project_links_alter_project_description_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('url', models.URLField()),
                ('task_name', models.ManyToManyField(to='main_app.task')),
            ],
        ),
        migrations.CreateModel(
            name='Journal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('date', models.DateField(verbose_name='journal entry date')),
                ('entry', models.TextField(max_length=5000)),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.task')),
            ],
        ),
        migrations.AddField(
            model_name='project',
            name='journals',
            field=models.ManyToManyField(to='main_app.journal'),
        ),
        migrations.AddField(
            model_name='project',
            name='youtube_tutorials',
            field=models.ManyToManyField(to='main_app.video'),
        ),
    ]
