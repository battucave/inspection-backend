# Generated by Django 4.0.6 on 2022-08-08 23:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0007_rename_single_iamge_property_single_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='property',
            name='single_image',
        ),
    ]
