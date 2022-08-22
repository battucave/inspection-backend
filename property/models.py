from django.db import models
from authapp.models import User

class Image(models.Model):
    image = models.ImageField(upload_to='thumbnails',blank=True,null=True)
    
class Documents(models.Model):
    document = models.FileField(upload_to='documents',blank=True,null=True)
    
class PropertyImage(models.Model):
    img = models.ForeignKey("Image", on_delete=models.CASCADE)
    property = models.ForeignKey("Property",on_delete=models.CASCADE)
    order = models.PositiveIntegerField(blank=True,null=True)
    


class RoomImage(models.Model):
    img = models.ForeignKey("Image", on_delete=models.CASCADE)
    room = models.ForeignKey("Room",on_delete=models.CASCADE)
    order = models.PositiveIntegerField(blank=True,null=True)

class PropertyType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
        
class Property(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    address = models.CharField(max_length=300)
    images = models.ManyToManyField(
        "Image", blank=True, through="PropertyImage"
    )
    property_type = models.ForeignKey("PropertyType",on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = "Properties"
    

class Room(models.Model):
    property = models.ForeignKey("Property",on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    images = models.ManyToManyField(  "Image", blank=True, through="RoomImage")

APPLICATION_STATE = [
    ("pending", "pending"),
    ("rejected", "rejected"),
    ("approved", "approved"),
    ("removed","removed"),
    
]

class PropertyApplication(models.Model):
    owner = models.ForeignKey(User, related_name="property_owner",on_delete=models.CASCADE,blank=True,null=True)
    tenant = models.ForeignKey(User,related_name="property_tenant",on_delete=models.CASCADE,blank=True,null=True)
    property = models.ForeignKey(Property,related_name="property_application" ,on_delete=models.CASCADE,blank=True,null=True)
    state = models.CharField(max_length=100, choices=APPLICATION_STATE,blank=True ,null=True)
    documents = models.ManyToManyField(
        "Documents", blank=True,
    )