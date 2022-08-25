from django.db import models
from authapp.models import User
from django.db.models import Q
from typing import Optional, Any
import uuid
from model_utils.models import TimeStampedModel, SoftDeletableModel, SoftDeletableManager
import datetime 
from django.utils import timezone


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return f"user_{instance.uploaded_by.pk}/{filename}"

    
class ConversationsModel(TimeStampedModel):
    id = models.BigAutoField(primary_key=True, verbose_name="Id")
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
        return ("Dialog between ") + f"{self.user_one_id}, {self.user_two_id}"

    @staticmethod
    def dialog_exists(u1: User, u2: User) -> Optional[Any]:
        return ConversationsModel.objects.filter(Q(user_one=u1, user_two=u2) | Q(user_one=u2, user_two=u1)).first()

    @staticmethod
    def create_if_not_exists(u1: User, u2: User):
        res = ConversationsModel.dialog_exists(u1, u2)
        if not res:
            ConversationsModel.objects.create(user_one=u1, user_two=u2)

    @staticmethod
    def get_dialogs_for_user(user: User):
        return ConversationsModel.objects.filter(Q(user_one=user) | Q(user_two=user)).order_by('-modified')
        #.values_list('user_one__pk', 'user_two__pk')
    
    
    def get_last_message_time(self):
        try:
            tm = MessageModel.objects.get(sender=self.user_one,recipient=self.user_two).get_last_message_for_dialog().created
        except:
            tm =self.created
        return tm

class UploadedFile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=("Uploaded_by"),
                                    related_name='+', db_index=True)
    file = models.FileField(verbose_name=("File"), blank=False, null=False, upload_to=user_directory_path)
    upload_date = models.DateTimeField(auto_now_add=True, verbose_name=("Upload date"))

    def __str__(self):
        return str(self.file.name)

class MessageModel(TimeStampedModel, SoftDeletableModel):
    sender = models.ForeignKey(User, related_name="message_sender",on_delete=models.CASCADE,blank=True,null=True)
    recipient = models.ForeignKey(User, related_name="message_recipient", on_delete=models.CASCADE,blank=True,null=True)
    text = models.TextField(verbose_name=("Text"), blank=True)
    image = models.ForeignKey(UploadedFile, related_name='message', on_delete=models.DO_NOTHING,
                             verbose_name=("Image"), blank=True, null=True)
    read = models.BooleanField(verbose_name="Read", default=False)

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
        #update the modified time of this Conversation
        dialog1 = ConversationsModel.objects.get(user_one=self.sender,user_two=self.recipient)
        dialog1.modified=timezone.now()
        dialog1.save()
        
        

    class Meta:
        ordering = ('-created',)
        verbose_name = ("Message")
        verbose_name_plural = ("Messages")


#Conversation.objects.filter(Q(user_one=b,user_two=a)|Q(user_one=a,user_two=b)) 
