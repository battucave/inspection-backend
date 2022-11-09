# chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

from authapp.models import User
from messaging.models import MessageModel, UploadedFile
import base64

from django.core.files.base import ContentFile

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['pk']
        self.room_group_name = 'chat_%s' % self.room_name
        
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)

        await self.save_message(text_data_json)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': text_data_json
            }
        )

    async def chat_message(self, event):
        message = event['message']

        await self.send(text_data=json.dumps({
            'message': message
        }))

    @sync_to_async
    def save_message(self, data):
        try:
            recipient = User.objects.get(pk=data.get("recipient"))
        except:
            self.close()

        try:
            sender = User.objects.get(pk=data.get("sender"))
        except:
            self.close()

        text = data.get('text')
        img_str = data.get('image')
        img_name = data.get('file_name')
        
        if img_str:
            file_obj = ContentFile(base64.b64decode(img_str), name=img_name)

            file_ = UploadedFile(file=file_obj,uploaded_by=sender)
            file_.save()
        else:
            file_=None
        
        msg = MessageModel(sender=sender,recipient=recipient,text=text,image=file_)
        msg.save()

        if file_:
            msg.image = file_
            msg.save()