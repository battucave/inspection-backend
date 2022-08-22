from django.db import models
from authapp.models import User
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from typing import Optional, Any
import uuid


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return f"user_{instance.uploaded_by.pk}/{filename}"

    
class ConversationsModel(models.Model):
    user_one = models.ForeignKey(User,related_name = "user_one",on_delete=models.CASCADE)
    user_two = models.ForeignKey(User,related_name = "user_two",on_delete=models.CASCADE)

    class Meta:
        unique_together = (('user_one', 'user_two'), ('user_two', 'user_one'),)
        

    def clean(self):
        if self.user_one and self.user_two and self.user_one.id>self.user_two.id:
            (self.user_one,self.user_two) = (self.user_two,self.user_one) 
    

    @classmethod
    def get(cls, userA, userB):
        """Gets all conversations between UserA and userB"""
        if userA.id>userB.id:
            (userA,userB)=(userB,userA)
        return cls.objects.filter(user_one=userA,user_two=userB)
    
    
  

    def __str__(self):
        return _("Dialog between ") + f"{self.user_one_id}, {self.user_two_id}"

    @staticmethod
    def dialog_exists(u1: User, u2: User) -> Optional[Any]:
        return ConversationsModel.objects.filter(Q(user1=u1, user2=u2) | Q(user1=u2, user2=u1)).first()

    @staticmethod
    def create_if_not_exists(u1: User, u2: User):
        res = ConversationsModel.dialog_exists(u1, u2)
        if not res:
            ConversationsModel.objects.create(user1=u1, user2=u2)

    @staticmethod
    def get_dialogs_for_user(user: User):
        return ConversationsModel.objects.filter(Q(user1=user) | Q(user2=user)).values_list('user_one__pk', 'user_two__pk')


class UploadedFile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("Uploaded_by"),
                                    related_name='+', db_index=True)
    file = models.FileField(verbose_name=_("File"), blank=False, null=False, upload_to=user_directory_path)
    upload_date = models.DateTimeField(auto_now_add=True, verbose_name=_("Upload date"))

    def __str__(self):
        return str(self.file.name)

class MessageModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    conversation = models.ForeignKey(ConversationsModel,on_delete=models.CASCADE)
    sender = models.ForeignKey(User, related_name="message_sender",on_delete=models.CASCADE,blank=True,null=True)
    recipient = models.ForeignKey(User, related_name="message_recipient", on_delete=models.CASCADE,blank=True,null=True)
    text = models.TextField(verbose_name=_("Text"), blank=True)
    file = models.ForeignKey(UploadedFile, related_name='message', on_delete=models.DO_NOTHING,
                             verbose_name=_("File"), blank=True, null=True)

    @staticmethod
    def get_unread_count_for_dialog_with_user(sender, recipient):
        return MessageModel.objects.filter(sender_id=sender, recipient_id=recipient, read=False).count()

    @staticmethod
    def get_last_message_for_dialog(sender, recipient):
        return MessageModel.objects.filter(
            Q(sender_id=sender, recipient_id=recipient) | Q(sender_id=recipient, recipient_id=sender)) \
            .select_related('sender', 'recipient').first()

    def __str__(self):
        return str(self.pk)

    def save(self, *args, **kwargs):
        super(MessageModel, self).save(*args, **kwargs)
        ConversationsModel.create_if_not_exists(self.sender, self.recipient)

    class Meta:
        ordering = ('-created',)
        verbose_name = _("Message")
        verbose_name_plural = _("Messages")


#Conversation.objects.filter(Q(user_one=b,user_two=a)|Q(user_one=a,user_two=b)) 
