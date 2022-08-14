from django.db import models
from authapp import User
class Conversation(models.Model):
    user_one = models.ForeignKey(User,related_name = "user_one")
    user_two = models.ForeignKey(User,related_name = "user_two")

    class Meta:
        unique_together = ('user_one','user_two')

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

