from inspection.settings import MEDIA_URL
from .models import ConversationsModel,MessageModel,UploadedFile
from rest_framework import serializers
from typing import Optional, Dict
import os
from authapp.models import User as UserModel




def serialize_file_model(m: UploadedFile) -> Dict[str, str]:
    return {'id': str(m.id), 'url': m.file.url,
            'size': m.file.size, 'name': os.path.basename(m.file.name)}


def serialize_message_model(m: MessageModel, user_id):
    sender_pk = m.sender.pk
    is_out = sender_pk == user_id
    # "read": m.read,
    obj = {
        "id": m.id,
        "text": m.text,
        "sent": int(m.created.timestamp()),
        "edited": int(m.modified.timestamp()),
       
        "image": serialize_file_model(m.image) if m.image else None,
        "sender": str(sender_pk),
        "recipient": str(m.recipient.pk),
        "out": is_out,
        "sender_username": m.sender.get_username()
    }
    return obj


def serialize_dialog_model(m: ConversationsModel, user_id):
    username_field = UserModel.USERNAME_FIELD
    other_user_pk, other_user_username, other_full_name, other_profile_picture = \
        UserModel.objects.filter(pk=m.user_one.pk).values_list('pk', username_field, 'full_name', 'profile_picture').first() \
        if m.user_two.pk == user_id else \
            UserModel.objects.filter(pk=m.user_two.pk).values_list('pk', username_field, 'full_name', 'profile_picture').first()
    unread_count = MessageModel.get_unread_count_for_dialog_with_user(sender=other_user_pk, recipient=user_id)
    last_message: Optional[MessageModel] = MessageModel.get_last_message_for_dialog(sender=other_user_pk,
                                                                                    recipient=user_id)
    last_message_ser = serialize_message_model(last_message, user_id) if last_message else None
    obj = {
        "id": m.id,
        "created": int(m.created.timestamp()),
        "modified": int(m.modified.timestamp()),
        "other_user_id": str(other_user_pk),
        "unread_count": unread_count,
        "username": other_user_username,
        "full_name": other_full_name,
        "profile_picture": MEDIA_URL+other_profile_picture,
        "last_message": last_message_ser
    }
    return obj
