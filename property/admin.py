from django.contrib import admin
from .models import *
# Register your models here.
class AdminTenant(admin.ModelAdmin):
    model = Tenant
    pass

admin.site.register(Tenant, AdminTenant)
admin.site.register(Property)
admin.site.register(PropertyImage)
admin.site.register(PropertyType)

admin.site.register(Discrepancy)

admin.site.register(Room)
admin.site.register(RoomImage)

admin.site.register(Image)




