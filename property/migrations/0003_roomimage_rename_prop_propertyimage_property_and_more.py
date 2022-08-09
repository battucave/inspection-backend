# Generated by Django 4.0.6 on 2022-08-08 16:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0002_propertyimage_order'),
    ]

    operations = [
        migrations.CreateModel(
            name='RoomImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveIntegerField()),
                ('img', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='property.image')),
            ],
        ),
        migrations.RenameField(
            model_name='propertyimage',
            old_name='prop',
            new_name='property',
        ),
        migrations.AddField(
            model_name='room',
            name='room_images',
            field=models.ManyToManyField(blank=True, through='property.RoomImage', to='property.image'),
        ),
        migrations.AlterField(
            model_name='property',
            name='address',
            field=models.CharField(max_length=300),
        ),
        migrations.AlterField(
            model_name='property',
            name='description',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='property',
            name='name',
            field=models.CharField(max_length=200),
        ),
        migrations.AddField(
            model_name='roomimage',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='property.room'),
        ),
    ]
