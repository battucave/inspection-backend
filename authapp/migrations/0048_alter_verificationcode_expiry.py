# Generated by Django 4.0.6 on 2022-11-08 19:26

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0047_alter_verificationcode_expiry'),
    ]

    operations = [
        migrations.AlterField(
            model_name='verificationcode',
            name='expiry',
            field=models.DateTimeField(default=datetime.datetime(2022, 11, 8, 19, 41, 58, 67954)),
        ),
    ]
