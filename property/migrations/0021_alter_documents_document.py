# Generated by Django 4.0.6 on 2022-08-22 03:55

from django.db import migrations, models
import property.models


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0020_alter_propertyapplication_documents'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documents',
            name='document',
            field=models.FileField(blank=True, null=True, upload_to='documents', validators=[property.models.validate_file_extension]),
        ),
    ]
