from django.db import models
from authapp.models import User

EMERGENCY_TYPES = [
    ("Hospital/Clinic", "Hospital/Clinic"),
    ("Fire Services", "Fire Services"),
    ("Ambulance Services", "Ambulance Services"),
        ("Rescue Services", "Rescue Services"),
    
]


class Emergency(models.Model):
    name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=20)
    state = models.CharField(max_length=20)
    zip_code = models.CharField(max_length=20)
    emergency_type = models.CharField(max_length=20,choices=EMERGENCY_TYPES,blank=True)
    user= models.ForeignKey(User,on_delete=models.CASCADE,blank=True)

    class Meta:
        verbose_name_plural = "Emergencies"
