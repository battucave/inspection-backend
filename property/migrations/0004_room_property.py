# Generated by Django 4.0.6 on 2022-08-08 21:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0003_roomimage_rename_prop_propertyimage_property_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='property',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='property.property'),
            preserve_default=False,
        ),
    ]
