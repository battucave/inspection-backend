# Generated by Django 4.0.6 on 2022-08-18 22:48

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0011_alter_verificationcode_expiry'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_maintenance',
        ),
        migrations.RemoveField(
            model_name='user',
            name='is_owner',
        ),
        migrations.RemoveField(
            model_name='user',
            name='is_vendor',
        ),
        migrations.RemoveField(
            model_name='user',
            name='is_verified',
        ),
        migrations.RemoveField(
            model_name='user',
            name='role',
        ),
        migrations.AddField(
            model_name='user',
            name='user_type',
            field=models.CharField(choices=[('owner', 'owner'), ('maintenance', 'maintenance'), ('vendor', 'vendor')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='verificationcode',
            name='expiry',
            field=models.DateTimeField(default=datetime.datetime(2022, 8, 19, 0, 3, 44, 404127)),
        ),
    ]
