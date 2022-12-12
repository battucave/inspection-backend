from django.db.models.signals import post_save
from django.dispatch import receiver
from property.models import Property, Tenant
from authapp.models import User

@receiver(post_save, sender=User)
def Check_user_property_tenant(sender, instance, created, **kwargs):
    if created:
        # when user created check if he has assigned properrity or not
        email = instance.email
        if email:
            # get emails and update attach them to user
            tenants = Tenant.objects.filter(email=email).update(user=instance)


@receiver(post_save, sender=Tenant)
def notify_tenant_with_property(sender, instance, created, **kwargs):
    if created:
        # when tenant created 
        email = instance.email
        user = User.objects.filter(email=email).first()
        if user:
            # notify user to login and check his email
            pass
        else:
            # notify user by email he is added
            pass


