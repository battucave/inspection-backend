from django.db import models
from authapp.models import User


class Report(models.Model):
    item = models.CharField(max_length=200)
    description = models.CharField(max_length=1000)
    photo = models.ImageField()
    claimed = models.BooleanField(default= False)
    claimed_by = models.ManyToManyField("User",blank=True)

REQUEST_STATE_CHOICES = [
        ('Open','Open'), 
        ('Close','Close'),
        ('Work_In_Progress','Work_In_Progress'),
        ]
REQUEST_TYPE_CHOICES = [
        ('Maintenance','Maintenance'), 
        ('Lost/Found','Lost/Found'),
        ]
class Request(models.Model):
    reqeust_type = models.CharField(max_length=10,
        choices= REQUEST_TYPE_CHOICES,
        default='Maintenance', blank=True,null=True)
    request_name = models.CharField()
    description = models.CharField()
    user = models.ForeignKey("User",on_delete=models.CASCADE)
    request_state =  models.CharField(
        max_length=10,
        choices= REQUEST_STATE_CHOICES,
        default='Open', blank=True,null=True
    )