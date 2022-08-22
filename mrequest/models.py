from django.db import models
from authapp.models import User
from property.models import Property

    

REQUEST_STATE_CHOICES = [
        ('Open','Open'), 
        ('Close','Close'),
        ('Work_In_Progress','Work_In_Progress'),
         ('Pending','Pending'),

        ]
REQUEST_TYPE_CHOICES = [
        ('Maintenance','Maintenance'), 
        ('Lost/Found','Lost/Found'),
        ]
class MRequest(models.Model):
    request_type = models.CharField(max_length=20,
        choices= REQUEST_TYPE_CHOICES,
        default='Maintenance', blank=True,null=True)
    request_name = models.CharField(max_length=200)
    description = models.CharField(max_length=100)
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="mrequest_user")
    request_state =  models.CharField(
        max_length=20,
        choices= REQUEST_STATE_CHOICES,
        default='Pending', blank=True,null=True
    )
    property = models.ForeignKey(Property,related_name="property_request",blank=True,null=True,on_delete=models.CASCADE)

#property owner must be able to manage requests