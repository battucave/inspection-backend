# Generated by Django 4.0.6 on 2022-08-22 02:43

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0024_alter_verificationcode_expiry'),
    ]

    operations = [
        migrations.AlterField(
            model_name='verificationcode',
            name='expiry',
            field=models.DateTimeField(default=datetime.datetime(2022, 8, 22, 3, 58, 17, 257317)),
        ),
    ]