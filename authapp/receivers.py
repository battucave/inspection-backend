from django.dispatch import receiver
from authapp.models import User,VerificationCode
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.mail import send_mail



@receiver(post_save, sender=VerificationCode)
def send_verification_email(sender, instance, **kwargs):
    user = instance.user
    to_ = user.email
    from_ = 'this@inspection.com'
    message = "Your verification code is {}".format(instance.code)
    send_mail('Inspection', message, from_, [to_], fail_silently=False)