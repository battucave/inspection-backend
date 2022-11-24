from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q


UserModel = get_user_model()


class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserModel.objects.get(Q(username__iexact=username) | Q(email__iexact=username))
        except UserModel.DoesNotExist:
            UserModel().set_password(password)
            return
        except UserModel.MultipleObjectsReturned:
            user = UserModel.objects.filter(Q(username__iexact=username) | Q(email__iexact=username)).order_by('id').first()

        if user.check_password(password) and self.user_can_authenticate(user):
            return user

from .models import User
from rest_framework import authentication
from rest_framework import exceptions
from firebase_admin import auth,initialize_app
initialize_app()
class FirebaseBackend(authentication.BaseAuthentication):
    def authenticate(self, request):
        authorization_header = request.META.get("HTTP_AUTHORIZATION")
        if not authorization_header:
            raise exceptions.AuthenticationFailed('Authorization credentials not provided')
        id_token = authorization_header.split(" ").pop()
        if not id_token:
            raise exceptions.AuthenticationFailed('Authorization credentials not provided')
        decoded_token = None
        try:
            decoded_token = auth.verify_id_token(id_token)
        except Exception:
            raise exceptions.AuthenticationFailed('Invalid ID Token')
        try:
            uid = decoded_token.get("uid")
        except Exception:
            raise exceptions.AuthenticationFailed('No such user exists')
        
        firebase_user = auth.get_user(uid=uid)

        user, created = User.objects.get_or_create(
            email=firebase_user.email,
            )
        if created:
            user.full_name = firebase_user.display_name
            user.phone = firebase_user.phone_number
            user.save()
        return (user, None)