# Generated by Django 4.0.6 on 2022-08-08 22:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0006_property_single_iamge'),
    ]

    operations = [
        migrations.RenameField(
            model_name='property',
            old_name='single_iamge',
            new_name='single_image',
        ),
    ]
