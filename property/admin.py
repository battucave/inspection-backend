from django.contrib import admin
from .models import *
from mrequest.models import MRequest
# Register your models here.
class TenantInline(admin.TabularInline):
    model = Tenant
    extra =1

class InspectionInline(admin.TabularInline):
    model = InspectionSchedule

class AdminTenant(admin.ModelAdmin):
    model = Tenant
    extra =1
class DiscrepancyInline(admin.TabularInline):
    model = Discrepancy
    extra=1

class InlineMRequest(admin.TabularInline):
    model = MRequest 
    extra =1
from django.utils.safestring import mark_safe

class InlineImages(admin.TabularInline):
    
    model = PropertyImage 
    extra =1
    readonly_fields = ["image_display"]

    def image_display(self, obj):
        if obj:
                return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
                    url = obj.img.image.url,
                    width="60px",
                    height="60px",
                    )
            )
        return "-----------"

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
     search_fields = ["name", ]
     inlines = [TenantInline, InspectionInline, DiscrepancyInline, InlineMRequest, InlineImages]



admin.site.register(Tenant, AdminTenant)

admin.site.register(Property)
admin.site.register(PropertyApplication)

admin.site.register(PropertyImage)
admin.site.register(PropertyType)

admin.site.register(Discrepancy)

admin.site.register(Room)
admin.site.register(RoomImage)

admin.site.register(Image)




