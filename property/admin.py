from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Property)
admin.site.register(PropertyImage)
admin.site.register(PropertyType)

admin.site.register(Discrepancy)

admin.site.register(Room)
admin.site.register(RoomImage)

admin.site.register(Image)


