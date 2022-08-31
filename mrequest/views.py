from rest_framework.views import APIView
from django.http import Http404
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from .serializers import MRequestSerializer,MListRequestSerializer
from .models import MRequest
from authapp.models import User
from rest_framework import generics
from rest_framework import filters 
from django_filters.rest_framework import DjangoFilterBackend
from property.models import Property

from inspection.permissions import CustomIsAuthenticatedPerm as IsAuthenticated
from inspection.pagination import CustomSuccessPagination


class RequestView(APIView):
    """Tenant living in a property can make a maintenance request"""
    serializer_class = MRequestSerializer
    permission_classes = (IsAuthenticated,)
    


    def get_object(self, pk):
        try:
            return MRequest.objects.get(pk=pk)
        except MRequest.DoesNotExist:
            return Response({'success':False,'error':True,'msg':'Request not found','data':{}},status=status.HTTP_200_OK)


    def post(self, request,pk):
        try:
            property = Property.objects.get(pk=pk)
        except:
            return Response({'success':False,'error':True,'msg':'Property not found','data':{}},status=status.HTTP_200_OK)
        if property.property_application.filter(tenant =request.user,state='approved'):
            serializer = MRequestSerializer(data=request.data)
        else:
            return Response({'success':False,'error':True,'msg':'You are not authorized to perform this action','data':{}},status=status.HTTP_200_OK)
        if serializer.is_valid():
            serializer.save(user=request.user,property=property)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    

class GetRequestView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = MRequestSerializer
   

    def get_object(self, pk):
        try:
            return MRequest.objects.get(pk=pk)
        except MRequest.DoesNotExist:
            return Response({'success':False,'error':True,'msg':'Request not found','data':{}},status=status.HTTP_200_OK)
    

    def get(self,request,pk):
        report = self.get_object(pk)
        serializer = MRequestSerializer(report)
        return Response({'success':True,'error':False,'msg':'','data':serializer.data},status=status.HTTP_200_OK)
    
    def put(self, request, pk, format=None):
        """Only owner of property can update request"""
        report = self.get_object(pk)
        serializer = MRequestSerializer(report, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'success':True,'error':False,'msg':'','data':serializer.data},status=status.HTTP_200_OK)
        return Response({'success':False,'error':True,'msg':'Request failed','data':serializer.data},status=status.HTTP_200_OK)
    
    
    def delete(self, request, pk, format=None):
        """Requestcreator can update request"""
        mrequest = self.get_object(pk)
        if request.user == mrequest.user:
            mrequest.delete()
            return Response({'success':True,'error':False,'msg':'','data':{}},status=status.HTTP_200_OK)
    
        return Response({'success':False,'error':True,'msg':'Operation failed','data':{}},status=status.HTTP_200_OK)
    
    

class ListRequestView(generics.ListAPIView):
    """List MRequest """
    permission_classes = (IsAuthenticated,)
    queryset = MRequest.objects.all()
    serializer_class = MListRequestSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user__id', 'request_state','request_type','property__id']
    pagination_class = CustomSuccessPagination


    