from django.db import models
from authapp.models import User
from datetime import datetime

class Report(models.Model):
    """
    claimed_by by are the users who claimed the lost item
    item_returned_user is the single user the item was returned to
    """
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=1000,blank=True)
    photo = models.ImageField(upload_to='reports',blank=True,null=True)
    claimed = models.BooleanField(default= False)
    claimed_by = models.ManyToManyField(User,blank=True,related_name="report_claimed_by")
    user = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    item_returned_user = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True,related_name="report_item_returned_user")
    returned = models.BooleanField(default= False)
    created_at = models.DateTimeField(auto_now_add=True)
    property = models.ForeignKey('property.Property',on_delete=models.CASCADE,blank=True,null=True)

    def __str__(self):
        return self.name
