# Generated by Django 4.0.6 on 2022-08-15 19:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0008_alter_verificationcode_expiry'),
    ]

    operations = [
        migrations.AlterField(
            model_name='verificationcode',
            name='created',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
