from django.db import models
from authapp.models import User
class Conversation(models.Model):
    user_one = models.ForeignKey(User,related_name = "user_one",on_delete=models.CASCADE)
    user_two = models.ForeignKey(User,related_name = "user_two",on_delete=models.CASCADE)

    class Meta:
        unique_together = (('user_one', 'user_two'), ('user_two', 'user_one'))
        

    def clean(self):
        if self.user_one and self.user_two and self.user_one.id>self.user_two.id:
            (self.user_one,self.user_two) = (self.user_two,self.user_one) 
    

    @classmethod
    def get(cls, userA, userB):
        """Gets all conversations between UserA and userB"""
        if userA.id>userB.id:
            (userA,userB)=(userB,userA)
        return cls.objects.filter(user_one=userA,user_two=userB)


class Messages(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    conversation = models.ForeignKey(Conversation,on_delete=models.CASCADE)
    sender = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)


#Conversation.objects.filter(Q(user_one=b,user_two=a)|Q(user_one=a,user_two=b)) 
