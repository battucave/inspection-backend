from django.db import models
from authapp.models import User


class Report(models.Model):
    item = models.CharField(max_length=200)
    description = models.CharField(max_length=1000)
    photo = models.ImageField()
    claimed = models.BooleanField(default= False)
    claimed_by = models.ManyToManyField(User,blank=True,related_name="report_claimed_by")

