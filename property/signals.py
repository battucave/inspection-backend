from django.db.models.signals import post_save
from django.dispatch import receiver
from property.models import Property, Tenant, InspectionSchedule, PropertyApplication
from authapp.models import User
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings


@receiver(post_save, sender=User)
def Check_user_property_tenant(sender, instance, created, **kwargs):
    
        if created:
            # when user created check if he has assigned properrity or not
            email = instance.email
            if email:
                # get emails and update attach them to user
                tenants = Tenant.objects.filter(email=email)
                if tenants:
                    tenants.update(user=instance)
                # mark user property applications as approved
                for tenant in tenants:
                    PropertyApplication.objects.get_or_create(
                        owner = tenant.property.user,
                        tenant = tenant.user,
                        property = tenant.property,
                        state = "approved",
                    )


@receiver(post_save, sender=Tenant)
def notify_tenant_with_property(sender, instance, created, **kwargs):
    if created:
        # when tenant created 
        email = instance.email
        user = User.objects.filter(email=email).first()
        context ={
                     "owner":instance.property.user.full_name,
                     "property":instance.property.name,
                     
                }
        if user:
            # create approved django application
            PropertyApplication.objects.get_or_create(
                    owner = instance.property.user,
                    tenant = instance.user,
                    property = instance.property,
                    state = "approved",
                )
            # notify user to login and check his account in app
            title = f"Inspection360 {instance.property.name} Invitation"
            email_html_message = render_to_string('email/proprty_tenant_user_email.html', context)
            email_plaintext_message = render_to_string('email/proprty_tenant_user_email.txt', context)
    
        else:
            # notify user by email he is added and he need to signup
            title = f"Inspection360 {instance.property.name} Invitation"
            email_html_message = render_to_string('email/tenant_user_signup_email.html', context)
            email_plaintext_message = render_to_string('email/tenant_user_signup_email.txt', context)
        from_email = settings.DEFAULT_FROM_EMAIL
        msg = EmailMultiAlternatives(
        # title:
        title,
        # message:
         email_plaintext_message,
        # from:
        from_email,
        # to:
        [email]
        )
        msg.attach_alternative(email_html_message, "text/html")
        msg.send()

# create inspectionschedule for each property
@receiver(post_save, sender=Property)
def create_inspection_schedule(sender, instance, created, **kwargs):
    if created:
         InspectionSchedule.objects.create(
            property=instance
         )