from rest_framework.views import APIView
from django.http import Http404
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from .serializers import EmergencySerializer
from .models import Emergency
from authapp.models import User
from rest_framework.pagination import LimitOffsetPagination 

from inspection.permissions import CustomIsAuthenticatedPerm as IsAuthenticated
from inspection.pagination import CustomSuccessPagination
class NewEmergencyView(APIView):
    """Only owner and vendor can create emergency contact"""
    serializer_class = EmergencySerializer
    permission_classes = (IsAuthenticated,)
    
    def get_object(self, pk):
        try:
            return Emergency.objects.get(pk=pk)
        except Emergency.DoesNotExist:
            return Response({'success':False,'error':True,'msg':'Emergency contact not found','data':{}},status=status.HTTP_200_OK)


    def post(self, request):
        serializer = EmergencySerializer(data=request.data)
        #print(request.user.user_type)
        if request.user.user_type=='maintenance':
            return Response({'success':False,'error':True,'msg':'Permission denied, only maintenance user can perform this action','data':{}},status=status.HTTP_200_OK)

        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({'success':True,'error':False,'msg':'Emergency contact created','data':serializer.data}, status=status.HTTP_201_CREATED)

        return Response({'success':False,'error':True,'msg':'Request failed','data':{}},status=status.HTTP_200_OK)




class GetEmergencyView(APIView):
    """Only owner and vendor can create emergency contact"""
    serializer_class = EmergencySerializer
    permission_classes = (IsAuthenticated,)
    
    
    def get_object(self, pk):
        try:
            return Emergency.objects.get(pk=pk)
        except Emergency.DoesNotExist:
            return Response({'success':False,'error':True,'msg':'Emergency contact not found','data':{}},status=status.HTTP_200_OK)

    

    def get(self,request,pk):
        emergency = self.get_object(pk)
        serializer = EmergencySerializer(emergency)
        return Response({'success':True,'error':False,'msg':'','data':serializer.data},status=status.HTTP_200_OK)

    
    def put(self, request, pk, format=None):
        emergency = self.get_object(pk)
        if request.user != emergency.user:
            return Response({'success':False,'error':True,'msg':'User not authorized to perform this action','data':{}},status=status.HTTP_200_OK)

        serializer = EmergencySerializer(emergency, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'success':True,'error':False,'msg':'Emergency contact updated','data':serializer.data},status=status.HTTP_200_OK)
        return Response({'success':False,'error':True,'msg':'Request failed','data':serializer.errors},status=status.HTTP_200_OK)
 
    def delete(self, request, pk, format=None):
        emergency = self.get_object(pk)
        if request.user == emergency.user:
            emergency.delete()
            return Response({'success':True,'error':False,'msg':'Emergency contact deleted','data':{}},status=status.HTTP_200_OK)
        return Response({'success':False,'error':True,'msg':'Request failed','data':{}},status=status.HTTP_200_OK)
    




class ListUserEmergency(APIView, CustomSuccessPagination):
    """Return emergency contacts of the user"""
    permission_classes = (IsAuthenticated,)
    

    def get(self,request):
        emergency = Emergency.objects.filter(user=request.user)
        results = self.paginate_queryset(emergency, request, view=self)
        property_serializer = EmergencySerializer(results, many=True)
        return self.get_paginated_response(property_serializer.data)