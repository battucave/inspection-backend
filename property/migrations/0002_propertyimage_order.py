# Generated by Django 4.0.6 on 2022-08-07 08:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='propertyimage',
            name='order',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
    ]
