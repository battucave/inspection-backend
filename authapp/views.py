from .models import User,VerificationCode
from .serializers import UserCreateSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
#from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from django.http import Http404

class CreateOwner(APIView):
    serializer_class = UserCreateSerializer
    permission_classes = ()
    authentication_classes = []

    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(is_owner=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateVendor(APIView):
    serializer_class = UserCreateSerializer
    permission_classes = ()
    authentication_classes = []

    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(is_vendor=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CreateMaintenance(APIView):
    serializer_class = UserCreateSerializer
    permission_classes = ()
    authentication_classes = []

    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(is_maintenance=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteUser(APIView):
    """Instead of deleting the account, set user as inactive"""
    serializer_class = UserCreateSerializer
    permission_classes = ()
    authentication_classes = [IsAuthenticated]
    
    """ Check that the request user is also the logged in user"""
    def get_object(self, pk):
        user = self.request.user
        kwarg_user = None

        try:
            kwarg_user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404
        if user == kwarg_user:
            return kwarg_user
        else:
            raise Http404

    def delete(self, request, pk):
        serializer = UserCreateSerializer(user= self.get_object(pk),data=request.data)
        if serializer.is_valid():
            serializer.save(is_active=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyCode(APIView):
    permission_classes = (IsAuthenticated,)
    """Check that verify code is correct"""
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
                return Response({'result':True},status=status.HTTP_200_OK)
        return  Response({'result':False},status=status.HTTP_200_OK)

class RefreshVerifyCode(APIView):
    permission_classes = (IsAuthenticated,)
    """Check that verify code is correct"""
    def get(self, request):
        VerificationCode.objects.create(user=request.user)
        return Response({'result':True},status=status.HTTP_201_CREATED)
        
