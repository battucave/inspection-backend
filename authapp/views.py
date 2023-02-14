from .models import User,VerificationCode
from .serializers import UserCreateSerializer, PasswordResetTokenSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
#from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from django.http import Http404
from .permissions import IsOwner

from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.models import update_last_login
from django.utils.translation import gettext_lazy as _
from rest_framework import exceptions, serializers
from rest_framework.exceptions import ValidationError
from rest_framework import generics

from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken, SlidingToken, UntypedToken

from rest_framework.parsers import MultiPartParser, FormParser
if api_settings.BLACKLIST_AFTER_ROTATION:
    from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken
from django_rest_passwordreset.views import (
    ResetPasswordRequestToken,
    ResetPasswordConfirm,
    ResetPasswordValidateToken,
)

from inspection.permissions import CustomIsAuthenticatedPerm as IsAuthenticated
from .backends import FirebaseBackend


class UploadUserImage(APIView):
    """Upload User Image"""
    permission_classes = (IsAuthenticated,)
    parser_classes = (MultiPartParser, FormParser,)
   
    
    def post(self, request):
        image = request.FILES.get('image')

        try:
            request.user.profile_picture = image
            request.user.save()
        except:
            return Response({'success':False,'error':True,'msg':'Error updating profile picture','data':{}},status=status.HTTP_200_OK)

        return Response({'success':True,'error':False,'msg':'Profile picture updated successfully','data':{}},status=status.HTTP_200_OK)
    
class UpdateUser(APIView):
    """Update User Profile"""
    permission_classes = (IsAuthenticated,)
    parser_classes = (MultiPartParser, FormParser,)
   
    
    def put(self, request):
        full_name = request.data.get('full_name')
        phone = request.data.get('phone')
        user_type = request.data.get('user_type')

        try:
            if(full_name):
                request.user.full_name = full_name
            if(phone):
                request.user.phone = phone
            if(user_type):
                request.user.user_type = user_type
            request.user.save()
        except:
            return Response({'success':False,'error':True,'msg':'Error updating profile information','data':{}},status=status.HTTP_200_OK)

        return Response({'success':True,'error':False,'msg':'Profile information updated successfully','data':{}},status=status.HTTP_200_OK)

class GetSingleUser(APIView):
    """Return user with the pk"""
    serializer_class = UserCreateSerializer
    permission_classes = (IsAuthenticated,)
    

    def get(self,request,pk):
        try:
            user = User.objects.get(pk=pk)
        except:
            return Response({'success':False,'error':True,'msg':'User not found','data':{}},status=status.HTTP_200_OK)
        serializer = UserCreateSerializer(user)
        return Response({'success':True,'error':False,'msg':'','data':serializer.data},status=status.HTTP_200_OK)

class VerifyFirebaseUser(APIView):
    serializer_class = UserCreateSerializer
    authentication_classes = [FirebaseBackend]

    def get(self, request):
        if not request.user:
            return Response({'success':False,'error':True,'msg':'User not authenticated','data':{}},status=status.HTTP_200_OK)
        serializer = UserCreateSerializer(request.user)
        return Response({'success':True,'error':False,'msg':'','data':serializer.data},status=status.HTTP_200_OK)

class CreateUser(APIView):
    """
    Create user
    """
    serializer_class = UserCreateSerializer
    permission_classes = ()
    authentication_classes = []
    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'success':True,'error':False,'msg':'Account created','data':serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'success':False,'error':True,'msg':'Error creating account','data':serializer.errors}, status=status.HTTP_200_OK)




class DeleteUser(APIView):
    """Instead of deleting the account, set user as inactive"""
    serializer_class = UserCreateSerializer
    permission_classes = (IsOwner,)
    
    """ Check that the request user is also the logged in user"""
    def get_object(self, pk):
        user = self.request.user
        kwarg_user = None

        try:
            kwarg_user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({'success':False,'error':True,'msg':'User doesnot exist','data':{}},status=status.HTTP_200_OK)
        if user == kwarg_user:
            return kwarg_user
        else:
            return Response({'success':False,'error':True,'msg':'You are not authorized to perform this action','data':{}},status=status.HTTP_200_OK)

    def delete(self, request, pk):
        user= self.get_object(pk)
        user.delete()
        return Response({'success':True,'error':False,'msg':'Account deleted','data':{}},status=status.HTTP_200_OK)

class VerifyCode(APIView):
    """Check that verify code is correct"""
    permission_classes = (IsAuthenticated,)
    
    def post(self, request):
        code = request.data['code']
        request_user_code = VerificationCode.objects.filter(user=request.user).last()
        #request_user_code = VerificationCode.objects.last()
        if request_user_code and code: 
            code_ = request_user_code.code
            if code_ == code:
                #user = User.objects.get(email=request.user)
                request.user.is_verified=True
                request.user.save()
                return Response({'success':True,'error':False,'msg':'Code verified','data':{'result':True}},status=status.HTTP_200_OK)
        return  Response({'success':False,'error':True,'msg':'Code verification failed','data':{'result':False}},status=status.HTTP_200_OK)

class RefreshVerifyCode(APIView):
    """Check that verify code is correct"""
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        VerificationCode.objects.create(user=request.user)
        return Response({'success':True,'error':False,'msg':'Refresh code generated','data':{'result':True}},status=status.HTTP_201_CREATED)
        


from rest_framework_simplejwt.views import TokenObtainPairView


class PasswordField(serializers.CharField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("style", {})

        kwargs["style"]["input_type"] = "password"
        kwargs["write_only"] = True

        super().__init__(*args, **kwargs)

class TokenObtainSerializer(serializers.Serializer):
    username_field = get_user_model().USERNAME_FIELD
    token_class = None

    default_error_messages = {
        "no_active_account": _("No active account found with the given credentials")
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields[self.username_field] = serializers.CharField()
        self.fields["password"] = PasswordField()

    def validate(self, attrs):
        authenticate_kwargs = {
            self.username_field: attrs[self.username_field],
            "password": attrs["password"],
        }
        try:
            authenticate_kwargs["request"] = self.context["request"]
        except KeyError:
            print("request not found")

        self.user = authenticate(**authenticate_kwargs)
        print("self usersss", self.user)
        if not self.user:
            return {'success':False,'error':True,'msg':'Authentication failed','data':{}}
        else:
            return {'success':True,'error':False,'msg':'Authentication successful','data':{}}


        

    @classmethod
    def get_token(cls, user):
        return cls.token_class.for_user(user)


class TokenObtainPairSerializer(TokenObtainSerializer):
    token_class = RefreshToken

    def validate(self, attrs):
        data = super().validate(attrs)
        if data['success']:
            refresh = self.get_token(self.user)
            data["data"]["refresh"] = str(refresh)
            data["data"]["access"] = str(refresh.access_token)

            if api_settings.UPDATE_LAST_LOGIN:
                update_last_login(None, self.user)

            return data
        else:
            return {'success':False,'error':True,'msg':'Authentication failed','data':{}}
        



class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer


from rest_framework import generics, status

from rest_framework_simplejwt.authentication import AUTH_HEADER_TYPES
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt import serializers as jwt_serializers
class TokenViewBase(generics.GenericAPIView):
    permission_classes = ()
    authentication_classes = ()

    serializer_class = None

    www_authenticate_realm = 'api'

    def get_authenticate_header(self, request):
        return '{0} realm="{1}"'.format(
            AUTH_HEADER_TYPES[0],
            self.www_authenticate_realm,
        )

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError:
            #raise InvalidToken(e.args[0])
            return Response({'success':False,'error':True,'msg':'Invalid token','data':{}}, status=status.HTTP_200_OK)

        return Response({'success':True,'error':False,'msg':'Token refreshed','data':serializer.validated_data}, status=status.HTTP_200_OK)

class TokenRefreshView(TokenViewBase):
    """
    Takes a refresh type JSON web token and returns an access type JSON web
    token if the refresh token is valid.
    """
    serializer_class = jwt_serializers.TokenRefreshSerializer



class PasswordResetView(ResetPasswordRequestToken):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            response.data["detail"] = "Password reset e-mail has been sent."
        return response


class PasswordResetConfirmView(ResetPasswordConfirm):
    serializer_class = PasswordResetTokenSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            response.data["detail"] = "Password has been reset successfuly"

        return response


class ResetPasswordVerifyToken(ResetPasswordValidateToken):
    def post(self, request, *args, **kwargs):

        response = super().post(request, *args, **kwargs)
        return response


