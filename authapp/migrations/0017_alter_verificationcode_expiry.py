# Generated by Django 4.0.6 on 2022-08-19 14:35

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0016_alter_verificationcode_expiry'),
    ]

    operations = [
        migrations.AlterField(
            model_name='verificationcode',
            name='expiry',
            field=models.DateTimeField(default=datetime.datetime(2022, 8, 19, 15, 49, 51, 657667)),
        ),
    ]
