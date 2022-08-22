# Generated by Django 4.0.6 on 2022-08-22 01:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import messaging.models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('messaging', '0002_messages_sender_alter_conversation_unique_together'),
    ]

    operations = [
        migrations.CreateModel(
            name='MessageModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('text', models.TextField(blank=True, verbose_name='Text')),
            ],
            options={
                'verbose_name': 'Message',
                'verbose_name_plural': 'Messages',
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='UploadedFile',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('file', models.FileField(upload_to=messaging.models.user_directory_path, verbose_name='File')),
                ('upload_date', models.DateTimeField(auto_now_add=True, verbose_name='Upload date')),
                ('uploaded_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Uploaded_by')),
            ],
        ),
        migrations.RenameModel(
            old_name='Conversation',
            new_name='ConversationsModel',
        ),
        migrations.DeleteModel(
            name='Messages',
        ),
        migrations.AddField(
            model_name='messagemodel',
            name='conversation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='messaging.conversationsmodel'),
        ),
        migrations.AddField(
            model_name='messagemodel',
            name='file',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='message', to='messaging.uploadedfile', verbose_name='File'),
        ),
        migrations.AddField(
            model_name='messagemodel',
            name='recipient',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='message_recipient', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='messagemodel',
            name='sender',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='message_sender', to=settings.AUTH_USER_MODEL),
        ),
    ]