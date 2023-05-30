import random
from django.dispatch import receiver
from authapp.models import User,VerificationCode
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives



@receiver(pre_save, sender=VerificationCode)
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

@receiver(pre_save, sender=User)
def generate_verification_code(sender, instance, **kwargs):
    has_code = VerificationCode.objects.filter(user=instance).last()
    if not instance.is_verified and not has_code:
        print('In coditions')
        VerificationCode.objects.create(user=instance, code="".join([str(random.randint(0,9)) for i in range(4)]))
    


from django_rest_passwordreset.signals import reset_password_token_created


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    """
    Handles password reset tokens
    When a token is created, an e-mail needs to be sent to the user
    :param sender: View Class that sent the signal
    :param instance: View Instance that sent the signal
    :param reset_password_token: Token Model Object
    :param args:
    :param kwargs:
    :return:
    """
    # send an e-mail to the user
    context = {
        'current_user': reset_password_token.user,
        'email': reset_password_token.user.email,
        # 'reset_password_url': "{}?token={}".format(
        #     instance.request.build_absolute_uri(reverse('password_reset:reset-password-confirm')),
        #     reset_password_token.key)
        'password_token': reset_password_token.key ,
    }
    # render email text
    message = "Your Password Reset code is {}".format(reset_password_token.key)
    email_html_message = render_to_string('email/user_reset_password.html', context)
    email_plaintext_message =message
    from_email = settings.DEFAULT_FROM_EMAIL

    msg = EmailMultiAlternatives(
        # title:
        "Password Reset for {title}".format(title=" Inspectio360"),
        # message:
        email_plaintext_message,
        # from:
        from_email,
        # to:
        [reset_password_token.user.email]
    )
    msg.attach_alternative(email_html_message, "text/html")
    msg.send()
