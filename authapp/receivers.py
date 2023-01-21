from django.dispatch import receiver
from authapp.models import User,VerificationCode
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives



@receiver(post_save, sender=VerificationCode)
def send_verification_email(sender, instance, **kwargs):
    user = instance.user
    to_ = user.email
    from_ = settings.DEFAULT_FROM_EMAIL
    context = {
        "verification_code":instance.code
    }
    message = "Your verification code is {}".format(instance.code)
    title = f"Inspection360 Account Verification"
    email_html_message = render_to_string('email/signup_verification_email.html', context)
    email_plaintext_message =message
    
    try:
        msg = EmailMultiAlternatives(
        # title:
        title,
        # message:
         email_plaintext_message,
        # from:
        from_,
        # to:
        [to_]
        )
        msg.attach_alternative(email_html_message, "text/html")
        msg.send()
    except:
        pass

@receiver(post_save, sender=User)
def generate_verification_code(sender, instance, **kwargs):
    if not instance.is_verified:
        VerificationCode.objects.create(user=instance)
    