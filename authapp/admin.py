from django.contrib import admin

# Register your models here.
from .models import User
from .forms import UserChangeForm, UserCreationForm

from property.models import Property


from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


class PropertyStackInline(admin.TabularInline):
    model = Property
    extra=1

class CustomUserAdmin(UserAdmin):
    #form = UserChangeForm
    #add_form = UserCreationForm
    model = User
    
    list_display = ('full_name','email',  'is_active',)
    list_filter = ('email',  'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    
    # add_fieldsets = (
    #     (None, {
    #         'classes': ('wide',),
    #         'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
    #     ),
    # )
    ordering = ('email',)
    search_fields = ["first_name", "username", "email"]
    #list_select_related = ("property",)
    inlines =(PropertyStackInline,)
    

admin.site.register(User, CustomUserAdmin)


