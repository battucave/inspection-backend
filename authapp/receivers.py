from django.dispatch import receiver
from authapp.models import User,VerificationCode
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.mail import send_mail
from django.conf import settings



@receiver(post_save, sender=VerificationCode)
def send_verification_email(sender, instance, **kwargs):
    user = instance.user
    to_ = user.email
    from_ = settings.DEFAULT_FROM_EMAIL
    message = "Your verification code is {}".format(instance.code)
    try:
        send_mail('Inspection', message, from_, [to_], fail_silently=False)
    except:
        pass

@receiver(post_save, sender=User)
def generate_verification_code(sender, instance, **kwargs):
    if not instance.is_verified:
        VerificationCode.objects.create(user=instance)
    