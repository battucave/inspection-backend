from django.contrib import admin
from .models import Property,PropertyType,Room,RoomImage,Image
# Register your models here.

admin.site.register(Property)
admin.site.register(PropertyType)

admin.site.register(Room)
admin.site.register(RoomImage)

admin.site.register(Image)

