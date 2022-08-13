from django.db import models
from authapp.models import User

class Image(models.Model):
    image = models.ImageField(upload_to='thumbnails',blank=True,null=True)
    

class PropertyImage(models.Model):
    img = models.ForeignKey("Image", on_delete=models.CASCADE)
    property = models.ForeignKey("Property",on_delete=models.CASCADE)
    order = models.PositiveIntegerField()
    


class RoomImage(models.Model):
    img = models.ForeignKey("Image", on_delete=models.CASCADE)
    room = models.ForeignKey("Room",on_delete=models.CASCADE)
    order = models.PositiveIntegerField()

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

class Room(models.Model):
    property = models.ForeignKey("Property",on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    room_images = models.ManyToManyField(  "Image", blank=True, through="RoomImage")

