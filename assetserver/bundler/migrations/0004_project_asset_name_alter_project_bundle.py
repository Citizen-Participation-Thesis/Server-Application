# Generated by Django 4.0.2 on 2022-03-03 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bundler', '0003_alter_project_bundle'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='asset_name',
            field=models.CharField(default='', max_length=80),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='project',
            name='bundle',
            field=models.FileField(upload_to='bundles'),
        ),
    ]
