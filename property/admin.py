from django.contrib import admin
from .models import *
# Register your models here.
class TenantInline(admin.TabularInline):
    model = Tenant

class AdminTenant(admin.ModelAdmin):
    model = Tenant

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
     inlines = [TenantInline]


admin.site.register(Tenant, AdminTenant)

admin.site.register(PropertyImage)
admin.site.register(PropertyType)

admin.site.register(Discrepancy)

admin.site.register(Room)
admin.site.register(RoomImage)

admin.site.register(Image)




