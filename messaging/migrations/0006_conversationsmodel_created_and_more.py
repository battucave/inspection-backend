# Generated by Django 4.0.6 on 2022-08-24 23:59

from django.db import migrations, models
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('messaging', '0005_remove_messagemodel_conversation'),
    ]

    operations = [
        migrations.AddField(
            model_name='conversationsmodel',
            name='created',
            field=model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created'),
        ),
        migrations.AddField(
            model_name='conversationsmodel',
            name='modified',
            field=model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified'),
        ),
        migrations.AlterField(
            model_name='conversationsmodel',
            name='id',
            field=models.BigAutoField(primary_key=True, serialize=False, verbose_name='Id'),
        ),
    ]
