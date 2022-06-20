# Generated by Django 4.0.2 on 2022-03-10 13:06

import colorfield.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bundler', '0005_materialprefix_modelfile_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hex_color', colorfield.fields.ColorField(default='#FFFFFF', image_field=None, max_length=18, samples=None)),
            ],
        ),
        migrations.AlterModelOptions(
            name='materialprefix',
            options={'verbose_name_plural': 'Material Prefixes'},
        ),
        migrations.AlterModelOptions(
            name='modelconfiguration',
            options={'verbose_name_plural': 'Model Configurations'},
        ),
        migrations.AlterModelOptions(
            name='modelfile',
            options={'verbose_name_plural': 'Raw Model Files'},
        ),
        migrations.AlterModelOptions(
            name='project',
            options={'verbose_name_plural': 'Projects'},
        ),
        migrations.RemoveField(
            model_name='materialprefix',
            name='hex_color',
        ),
        migrations.RemoveField(
            model_name='project',
            name='material_prefixes',
        ),
        migrations.AddField(
            model_name='modelfile',
            name='prefixes',
            field=models.ManyToManyField(to='bundler.MaterialPrefix'),
        ),
        migrations.AddField(
            model_name='materialprefix',
            name='materials',
            field=models.ManyToManyField(max_length=1, to='bundler.Material'),
        ),
    ]