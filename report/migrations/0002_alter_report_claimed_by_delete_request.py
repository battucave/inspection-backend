# Generated by Django 4.0.6 on 2022-08-14 21:09

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('report', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='claimed_by',
            field=models.ManyToManyField(blank=True, related_name='report_claimed_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='Request',
        ),
    ]
