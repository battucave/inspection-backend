from django.db import models
from authapp.models import User
from django.core.exceptions import ValidationError
from datetime import date

def validate_file_extension(value):
    if not value.name.endswith('.pdf'):
        raise ValidationError(u'Error message')

class Image(models.Model):
    image = models.ImageField(upload_to='thumbnails',blank=True,null=True)
    
class Documents(models.Model):
    document = models.FileField(upload_to='documents',blank=True,null=True,validators=[validate_file_extension])
    
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
    
class Tenant(models.Model):
    email = models.EmailField(verbose_name="Email")
    user = models.ForeignKey(User,on_delete=models.SET_NULL, null=True, blank=True)
    property = models.ForeignKey(to=Property, on_delete=models.CASCADE)

    # class Meta:
    #         unique_together = ("email", "property")


    

class InspectionSchedule(models.Model):
    property = models.OneToOneField(to=Property, on_delete=models.CASCADE)
    period = models.SmallIntegerField(verbose_name="inspection interval with day",
    help_text=" setting period between inspection by days", null=True, blank=True)
    last_triggered = models.DateField(default=date.today)


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

class Section(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='thumbnails',blank=True,null=True)

class CheckInRoomSection(models.Model):
    img = models.ForeignKey("Section", on_delete=models.CASCADE)
    room_occupancy = models.ForeignKey("RoomOccupancy",on_delete=models.CASCADE)

class CheckOutRoomSection(models.Model):
    img = models.ForeignKey("Section", on_delete=models.CASCADE)
    room_occupancy = models.ForeignKey("RoomOccupancy",on_delete=models.CASCADE)

class RoomOccupancy(models.Model):
    name = models.CharField(max_length=100)
    check_in_images = models.ManyToManyField("Section", related_name="check_in_images", blank=True, through="CheckInRoomSection")
    check_out_images = models.ManyToManyField("Section", related_name="check_out_images", blank=True, through="CheckOutRoomSection")
    tenant = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    property = models.ForeignKey(Property,on_delete=models.CASCADE,blank=True,null=True)
    room = models.ForeignKey("Room",on_delete=models.CASCADE,blank=True,null=True)

DISCREPANCY_TIME = [
    ("check-in", "check-in"),
    ("check-out", "check-out"),
]

class Discrepancy(models.Model):
    property = models.ForeignKey("Property",on_delete=models.CASCADE)
    room_occupancy = models.ForeignKey("RoomOccupancy",on_delete=models.CASCADE)
    expected_image = models.ForeignKey("Image",related_name="expected_image",on_delete=models.CASCADE,blank=True,null=True)
    uploaded_image = models.ForeignKey("Section",on_delete=models.CASCADE,blank=True,null=True)
    discrepancy_at = models.CharField(max_length=100, choices=DISCREPANCY_TIME)
    diff = models.PositiveIntegerField(blank=True,null=True)
    diff_image = models.ForeignKey("Image",related_name="difference_image", on_delete=models.CASCADE)


    def __str__(self) -> str:
        try:
            property_name = self.property.name
            return property_name
        except:       
            return super().__str__()