# Generated by Django 4.0.6 on 2022-08-22 03:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0004_rename_item_report_name_alter_report_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='description',
            field=models.CharField(blank=True, max_length=1000),
        ),
    ]
