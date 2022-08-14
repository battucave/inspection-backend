from django.db import models
from authapp.models import User



    

REQUEST_STATE_CHOICES = [
        ('Open','Open'), 
        ('Close','Close'),
        ('Work_In_Progress','Work_In_Progress'),
        ]
REQUEST_TYPE_CHOICES = [
        ('Maintenance','Maintenance'), 
        ('Lost/Found','Lost/Found'),
        ]
class MRequest(models.Model):
    reqeust_type = models.CharField(max_length=20,
        choices= REQUEST_TYPE_CHOICES,
        default='Maintenance', blank=True,null=True)
    request_name = models.CharField(max_length=100)
    description = models.CharField(max_length=400)
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="mrequest_user")
    request_state =  models.CharField(
        max_length=20,
        choices= REQUEST_STATE_CHOICES,
        default='Open', blank=True,null=True
    )