from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.http import Http404
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from .serializers import EmergencySerializer
from .models import Emergency
from authapp.models import User
from rest_framework.pagination import LimitOffsetPagination 

class NewEmergencyView(APIView):
    """Only owner and vendor can create emergency contact"""
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



class GetEmergencyView(APIView):
    """Only owner and vendor can create emergency contact"""
    serializer_class = EmergencySerializer
    permission_classes = (IsAuthenticated,)
    
    
    def get_object(self, pk):
        try:
            return Emergency.objects.get(pk=pk)
        except Emergency.DoesNotExist:
            raise Http404
    

    def get(self,request,pk):
        emergency = self.get_object(pk)
        serializer = EmergencySerializer(emergency)
        return Response(serializer.data)
    
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
    




class ListUserEmergency(APIView, LimitOffsetPagination):
    """Return emergency contacts of the user"""
    permission_classes = (IsAuthenticated,)
    

    def get(self,request):
        emergency = Emergency.objects.filter(user=request.user)
        results = self.paginate_queryset(emergency, request, view=self)
        property_serializer = EmergencySerializer(results, many=True)
        return self.get_paginated_response(property_serializer.data)