from django.db.models.signals import post_save
from django.dispatch import receiver
from property.models import Property, Tenant
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
            tenants = Tenant.objects.filter(email=email).update(user=instance)


@receiver(post_save, sender=Tenant)
def notify_tenant_with_property(sender, instance, created, **kwargs):
    if created:
        # when tenant created 
        email = instance.email
        user = User.objects.filter(email=email).first()
        context ={
                    "property_owner":instance.property.user,
                     "property":instance.property.name,
                     
                }
        if user:
            # notify user to login and check his email
            title = f"Inspection360 {instance.property.name} Invitation"
            email_html_message = render_to_string('email/proprty_tenant_user_email.html', context)
            email_plaintext_message = render_to_string('email/proprty_tenant_user_email.txt', context)
    
        else:
            # notify user by email he is added

            title = f"Inspection360 {instance.property.name} Invitation"
            email_html_message = render_to_string('email/tenant_user_signup_email.html', context)
            email_plaintext_message = render_to_string('email/ptenant_user_signup_email.txt', context)
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
