from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.http import Http404
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from .serializers import MRequestSerializer
from .models import MRequest
from authapp.models import User
from rest_framework import generics
from rest_framework import filters 
from django_filters.rest_framework import DjangoFilterBackend
from property.models import Property

from rest_framework.pagination import LimitOffsetPagination
class RequestView(APIView):
    """Tenant living in a property can make a maintenance request"""
    serializer_class = MRequestSerializer
    permission_classes = (IsAuthenticated,)
    


    def get_object(self, pk):
        try:
            return MRequest.objects.get(pk=pk)
        except MRequest.DoesNotExist:
            raise Http404

    def post(self, request,pk):
        try:
            property = Property.objects.get(pk=pk)
        except:
            raise Http404
        if property.property_application.filter(tenant =request.user,state='approved'):
            serializer = MRequestSerializer(data=request.data)
        else:
            raise Http404
        if serializer.is_valid():
            serializer.save(user=request.user,property=property)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format=None):
        """Only owner of property can update request"""
        report = self.get_object(pk)
        serializer = MRequestSerializer(report, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        """Requestcreator can update request"""
        mrequest = self.get_object(pk)
        if request.user == mrequest.user:
            mrequest.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)

class GetRequestView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = MRequestSerializer
   

    def get_object(self, pk):
        try:
            return MRequest.objects.get(pk=pk)
        except MRequest.DoesNotExist:
            raise Http404
    

    def get(self,request,pk):
        report = self.get_object(pk)
        serializer = MRequestSerializer(report)
        return Response(serializer.data)
    

class ListRequestView(generics.ListAPIView):
    """List MRequest """
    permission_classes = (IsAuthenticated,)
    queryset = MRequest.objects.all()
    serializer_class = MRequestSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user__id', 'request_state','request_type','property__id']


    