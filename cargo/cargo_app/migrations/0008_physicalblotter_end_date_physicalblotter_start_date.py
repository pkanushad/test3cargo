# Generated by Django 4.1.2 on 2022-10-29 20:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cargo_app', '0007_physicalblotter_bl_date_physicalblotter_density_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='physicalblotter',
            name='end_date',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='physicalblotter',
            name='start_date',
            field=models.DateField(null=True),
        ),
    ]
