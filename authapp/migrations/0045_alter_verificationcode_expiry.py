# Generated by Django 4.0.6 on 2022-11-08 18:42

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0044_alter_verificationcode_expiry'),
    ]

    operations = [
        migrations.AlterField(
            model_name='verificationcode',
            name='expiry',
            field=models.DateTimeField(default=datetime.datetime(2022, 11, 8, 18, 57, 9, 261081)),
        ),
    ]
