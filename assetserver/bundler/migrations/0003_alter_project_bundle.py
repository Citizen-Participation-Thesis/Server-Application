# Generated by Django 4.0.2 on 2022-03-03 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bundler', '0002_alter_project_bundle'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='bundle',
            field=models.FileField(upload_to=''),
        ),
    ]
