# Generated by Django 4.0.6 on 2022-08-19 01:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0015_alter_property_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='roomimage',
            name='order',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
