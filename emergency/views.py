from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.http import Http404
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from .serializers import EmergencySerializer
from .models import Emergency
from authapp.models import User

class EmergencyView(APIView):
    
    serializer_class = EmergencySerializer
    permission_classes = (IsAuthenticated,)
    

  
    def get_object(self, pk):
        try:
            return Emergency.objects.get(pk=pk)
        except Emergency.DoesNotExist:
            raise Http404

    def post(self, request):
        serializer = EmergencySerializer(data=request.data)
        print(request.user.user_type)
        if request.user.user_type=='maintenance':
            raise Http404("Permission denied")
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format=None):
        emergency = self.get_object(pk)
        if request.user != emergency.user:
            raise Http404
        serializer = EmergencySerializer(emergency, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        emergency = self.get_object(pk)
        if request.user == emergency.user:
            emergency.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class GetEmergencyView(APIView):
    queryset = Emergency.objects.all()
    serializer_class = EmergencySerializer
    

    def get_object(self, pk):
        try:
            return Emergency.objects.get(pk=pk)
        except Emergency.DoesNotExist:
            raise Http404
    

    def get(self,request,pk):
        emergency = self.get_object(pk)
        serializer = EmergencySerializer(emergency)
        return Response(serializer.data)
    

class GetUserEmergency(APIView):
    """Return emergency contacts of the user with the pk"""
    permission_classes = (IsAuthenticated,)
    

    def get(self,request,pk):
        try:
            user = User.objects.get(pk=pk)
        except:
            user = None

        result = Emergency.objects.filter(user=user)
        emergency_serializer = EmergencySerializer(result, many=True)
        return Response(emergency_serializer.data)