from django.contrib import admin
from .models import MessageModel, ConversationsModel
# Register your models here.

admin.site.register(MessageModel)
admin.site.register(ConversationsModel)
