from django.core.exceptions import ValidationError
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework import generics
from django.http import Http404
from rest_framework.parsers import MultiPartParser, FormParser
from .models import *
from .serializers import *
from authapp.permissions import  IsOwner, IsOwnerOrReadOnly
from authapp.models import User
from rest_framework import filters 
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from django.shortcuts import get_object_or_404
from inspection.permissions import CustomIsAuthenticatedPerm as IsAuthenticated
from inspection.pagination import CustomSuccessPagination

class NewProperty(APIView):
    """Create single property"""
    permission_classes = (IsAuthenticated,)
    parser_classes = (MultiPartParser, FormParser,)
    serializer_class = PropertySerializer
    def get_parsers(self):
        if getattr(self, 'swagger_fake_view', False):
            return []

        return super().get_parsers()

    def get_object(self, pk):
        try:
            return Property.objects.get(pk=pk)
        except Property.DoesNotExist:
            return Response({'success':False,'error':True,'msg':'Property not found','data':{}},status=status.HTTP_200_OK)

   
    #@action(detail=False, methods=['post'], parser_classes=(FormParser, ))
    #@swagger_auto_schema(request_body=PropertySerializer)
    def post(self, request):
        serializer = PropertySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({'success':True,'error':False,'msg':'Property created','data':serializer.data},status=status.HTTP_201_CREATED)
    
        return Response({'success':False,'error':True,'msg':'Error creating property','data':serializer.errors},status=status.HTTP_200_OK)
    
    
    

class GetProperty(APIView):
    """Update,Delete for single property"""
    permission_classes = (IsOwnerOrReadOnly,)
    parser_classes = (MultiPartParser, FormParser,)
    serializer_class = PropertySerializer
    def get_parsers(self):
        if getattr(self, 'swagger_fake_view', False):
            return []

        return super().get_parsers()

    def get_object(self, pk):
        try:
            return Property.objects.get(pk=pk)
        except Property.DoesNotExist:
            return Response({'success':False,'error':True,'msg':'Property not found','data':{}},status=status.HTTP_200_OK)
    def get(self,request,pk):
        """Return single property"""
        emergency = self.get_object(pk)
        serializer = PropertySerializer(emergency)
        return Response({'success':True,'error':False,'msg':'','data':serializer.data},status=status.HTTP_200_OK)
    
    
    
    def put(self, request, pk, format=None):
        """Update property"""
        emergency = self.get_object(pk)
        serializer = PropertySerializer(emergency, data=request.data)
        print(serializer)
        if serializer.is_valid():
            serializer.save()
            return Response({'success':True,'error':False,'msg':'','data':serializer.data},status=status.HTTP_200_OK)
    
        return Response({'success':True,'error':False,'msg':'','data':serializer.errors},status=status.HTTP_200_OK)
    
    
    
    def delete(self, request, pk, format=None):
        """Delete Property"""
        property = self.get_object(pk)
        if property.user == request.user:
            property.delete()
            return Response({'success':True,'error':False,'msg':'Property deleted','data':{}},status=status.HTTP_200_OK)
        return Response({'success':False,'error':True,'msg':'Operation failed','data':{}},status=status.HTTP_200_OK)
    
    
        

class PropertyTypeView(APIView):
    """Return all property types"""
    def get(self,request):
        property_types = PropertyType.objects.all()
        property_type_serializer = PropertyTypeSerializer(property_types, many=True)
        return Response({'success':True,'error':False,'msg':'','data':property_type_serializer.data},status=status.HTTP_200_OK)




class PropertySearchView(generics.ListAPIView):
    """Property search"""
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description','address']
    pagination_class = CustomSuccessPagination

class AllProperty(APIView, CustomSuccessPagination):
    """Return all properties"""
    def get(self,request):
        properties = Property.objects.all()
        results = self.paginate_queryset(properties, request, view=self)
        serializer = PropertySerializer(results, many=True)
        return self.get_paginated_response(serializer.data)
        

class UserProperty(APIView, CustomSuccessPagination):
    """Return properties of the logged in user"""
    permission_classes = (IsAuthenticated,)
    

    def get(self,request):
        properties = Property.objects.filter(user=request.user)
        results = self.paginate_queryset(properties, request, view=self)
        property_serializer = PropertySerializer(results, many=True)
        return self.get_paginated_response(property_serializer.data)

class GetUserProperty(APIView,CustomSuccessPagination):
    """Return properties of the user with the pk"""
    permission_classes = (IsAuthenticated,)
    

    def get(self,request,pk):
        try:
            user = User.objects.get(pk=pk)
        except:
            user = None

        properties = Property.objects.filter(user=user)
        results = self.paginate_queryset(properties, request, view=self)
        property_serializer = PropertySerializer(results, many=True)
        return self.get_paginated_response(property_serializer.data)

    
class NewRoom(APIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = RoomSerializer
    

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            return Response({'success':False,'error':True,'msg':'Room not found','data':{}},status=status.HTTP_200_OK)
        
    def post(self, request,pk):
        try:
            property =Property.objects.get(pk=pk)
        except Property.DoesNotExist:
            return Response({'success':False,'error':True,'msg':'Property not found','data':{}},status=status.HTTP_200_OK)
        serializer = RoomSerializer(data=request.data)
        if property.user != request.user:
            return Response({'success':False,'error':True,'msg':'User not authorized to perform this action','data':{}},status=status.HTTP_200_OK)
    
        if serializer.is_valid():
            serializer.save(property=property)
            return Response({'success':True,'error':False,'msg':'','data':serializer.data},status=status.HTTP_201_CREATED)
    
        return Response({'success':False,'error':True,'msg':'Error creating room','data':serializer.errors},status=status.HTTP_200_OK)
    
    


class RoomView(APIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = RoomSerializer
    

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            return Response({'success':False,'error':True,'msg':'Room not found','data':''},status=status.HTTP_200_OK)
    def get(self,request,pk):
        room = self.get_object(pk)
        serializer = RoomSerializer(room)
        return Response({'success':True,'error':False,'msg':'','data':serializer.data},status=status.HTTP_200_OK)
        
   
    def put(self, request, pk, format=None):
        room = self.get_object(pk)
        if room.property.user != request.user:
            return Response({'success':False,'error':True,'msg':'User not authorized to perform this action','data':{}},status=status.HTTP_200_OK)
        
        serializer = RoomSerializer(room, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'success':True,'error':False,'msg':'','data':serializer.data},status=status.HTTP_200_OK)
        
        return Response({'success':False,'error':True,'msg':'Error updating room','data':serializer.errors},status=status.HTTP_200_OK)
        
    
    
    def delete(self, request, pk, format=None):
        room = self.get_object(pk)
        if room.property.user == request.user:
            room.delete()
            return Response({'success':True,'error':False,'msg':'Room deleted','data':{}},status=status.HTTP_200_OK)
        
        return Response({'success':False,'error':True,'msg':'Error deleting room','data':{}},status=status.HTTP_200_OK)
        
class PropertyRooms(APIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = RoomSerializer

    def get_object(self, pk):
        try:
            return Property.objects.get(pk=pk)
        except Property.DoesNotExist:
            return Response({'success':False,'error':True,'msg':'Property not found','data':{}},status=status.HTTP_200_OK)
        
    def get(self,request,pk):
        property = self.get_object(pk)
        rooms = Room.objects.filter(property=property)
        serializer = RoomSerializer(rooms,many=True)
        return Response({'success':True,'error':False,'msg':'','data':serializer.data},status=status.HTTP_200_OK)
        


class NewPropertyApplication(APIView):
    """Create new property application"""
    permission_classes = (IsAuthenticated,)
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = PropertyApplicationSerializer
    

    def get_object(self, pk):
        try:
            return Property.objects.get(pk=pk)
        except Property.DoesNotExist:
            raise Http404
    #@swagger_auto_schema(request_body=PropertyApplicationSerializer)
    def post(self, request,pk):
        try:
            property =Property.objects.get(pk=pk)
        except Property.DoesNotExist:
            return Response({'success':False,'error':True,'msg':'Property not found','data':{}},status=status.HTTP_200_OK)

        serializer = PropertyApplicationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(property=property, owner=property.user,tenant=request.user,state='pending')
            return Response({'success':True,'error':False,'msg':'Property application created','data':serializer.data},status=status.HTTP_201_CREATED)
    
        return Response({'success':False,'error':True,'msg':'Error creating Request','data':serializer.errors},status=status.HTTP_200_OK)


class PropertyApplicationUpdate(APIView):
    """Property application can only be updated by owner"""
    permission_classes = (IsAuthenticated,)
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = PropertyApplicationSerializer
    

    def get_object(self, pk):
        try:
            return Property.objects.get(pk=pk)
        except Property.DoesNotExist:
            return Response({'success':False,'error':True,'msg':'Property not found','data':{}},status=status.HTTP_200_OK)

        
    def put(self, request,pk):
        """Only owner can edit property application"""
        try:
            property = PropertyApplication.objects.get(pk=pk)
        except PropertyApplication.DoesNotExist:
            return Response({'success':False,'error':True,'msg':'Property application not found','data':{}},status=status.HTTP_200_OK)

        if request.user != property.owner:
            return Response({'success':False,'error':True,'msg':'You are not authorized to change this application','data':{}},status=status.HTTP_200_OK)

        serializer = PropertyApplicationSerializer(property, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'success':True,'error':False,'msg':'Request created','data':serializer.data},status=status.HTTP_201_CREATED)
        return Response({'success':False,'error':True,'msg':'Error creating Request','data':serializer.errors},status=status.HTTP_200_OK)
    
class PropertyApplications(generics.ListAPIView):
    """List Property Applications """
    permission_classes = (IsAuthenticated,)
    queryset = PropertyApplication.objects.all()
    serializer_class = ListPropertyApplicationSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['owner__id', 'tenant__id','state']
    pagination_class = CustomSuccessPagination

class ListTenantProperties(APIView,CustomSuccessPagination):
    permission_classes = (IsAuthenticated,)
    """Return properties where the request user is an approved tenant"""
    def get(self,request):
        properties = Property.objects.filter(property_application__tenant =request.user,property_application__state='approved') 
        results = self.paginate_queryset(properties, request, view=self)
        property_serializer = PropertySerializer(results, many=True)
        return self.get_paginated_response(property_serializer.data)

class ListTenantPropertiesnew(APIView,CustomSuccessPagination):
    permission_classes = (IsAuthenticated,)
    """Return properties where the request user is an approved tenant"""
    def get(self,request):
        properties = Property.objects.filter(property_application__tenant =request.user,property_application__state='approved') 
        results = self.paginate_queryset(properties, request, view=self)
        property_serializer = PropertySerializer(results, many=True)
        return self.get_paginated_response(property_serializer.data)

class RoomOccupancyAPI(APIView):
    # permission_classes = (IsAuthenticated,)
    parser_classes = (MultiPartParser, FormParser,)
    serializer_class = RoomOccupancySerializer
    
    def get_object(self, id):
        try:
            return RoomOccupancy.objects.get(id=id)
        except RoomOccupancy.DoesNotExist:
            return Response({'success':False,'error':True,'msg':'Property not found','data':{}},status=status.HTTP_200_OK)

    def get_property(self, pk):
        try:
            return Property.objects.get(pk=pk)
        except Property.DoesNotExist:
            return Response({'success':False,'error':True,'msg':'Property not found','data':{}},status=status.HTTP_200_OK)

    def get_room(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            return Response({'success':False,'error':True,'msg':'Room not found','data':{}},status=status.HTTP_200_OK)

    def get(self, request, id):
        room = self.get_object(id)
        serializer = RoomOccupancySerializer(room)
        return Response({'success':True,'error':False,'data':serializer.data},status=status.HTTP_200_OK)

    def post(self, request):
        serializer = RoomOccupancySerializer(data = request.data)
        property = self.get_property(request.data.get('property'))
        room = self.get_room(request.data.get('room'))
        if serializer.is_valid(raise_exception=True):
            serializer.save(property=property, room=room)
            return Response({'success':True,'error':False,'data':serializer.data},status=status.HTTP_200_OK)

        return Response({'success':False,'error':True,'msg':serializer.errors,},status=status.HTTP_200_OK)

class ListRoomOccupancys(generics.ListAPIView):
    # permission_classes = (IsAuthenticated,)
    queryset = RoomOccupancy.objects.all()
    serializer_class = ListRoomOccupancySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['tenant__id', 'property__id', 'room__id']
    pagination_class = CustomSuccessPagination

class SectionAPI(APIView):
    # permission_classes = (IsAuthenticated,)
    parser_classes = (MultiPartParser, FormParser,)

    def post(self, request):
        serializer = SectionSerializer(data = request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response({'success':True,'error':False,'data':serializer.data},status=status.HTTP_200_OK)

        return Response({'success':False,'error':True,'msg':serializer.errors,},status=status.HTTP_200_OK)

class CheckInAndSection(APIView):
    # permission_classes = (IsAuthenticated,)
    parser_classes = (MultiPartParser, FormParser,)

    def get_object(self, id):
        try:
            return RoomOccupancy.objects.get(id=id)
        except RoomOccupancy.DoesNotExist:
            return Response({'success':False,'error':True,'msg':'Room not found','data':{}},status=status.HTTP_200_OK)

    def post(self, request,id):

        room_occupancy = self.get_object(id)
        serializer = CompareSectionSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save(
             room_occupancy=room_occupancy,
             property=room_occupancy.property,
             room=room_occupancy.room,
             event='check-in',
             expected_image=request.data.get('expected_image')
            )
            section = Section.objects.get(pk=serializer.data['id'])
            room_occupancy.check_in_images.add(section)
            room_occupancy.save()
            return Response({'success':True,'error':False,'msg':'Request created','data':serializer.data},status=status.HTTP_200_OK)
        return Response({'success':False,'error':True,'msg':'Error creating Request','data':serializer.errors},status=status.HTTP_200_OK)

class CheckOutAndSection(APIView):
    parser_classes = (MultiPartParser, FormParser,)

    def get_object(self, id):
        try:
            return RoomOccupancy.objects.get(id=id)
        except RoomOccupancy.DoesNotExist:
            return Response({'success':False,'error':True,'msg':'Room not found','data':{}},status=status.HTTP_200_OK)

    def post(self, request,id):

        room_occupancy = self.get_object(id)
        serializer = CompareSectionSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save(
             room_occupancy=room_occupancy,
             property=room_occupancy.property,
             room=room_occupancy.room,
             event='check-out',
             expected_image=request.data.get('expected_image')
            )
            section = Section.objects.get(pk=serializer.data['id'])
            room_occupancy.check_out_images.add(section)
            room_occupancy.save()
            return Response({'success':True,'error':False,'msg':'Request created','data':serializer.data},status=status.HTTP_200_OK)
        return Response({'success':False,'error':True,'msg':'Error creating Request','data':serializer.errors},status=status.HTTP_200_OK)

class ListDiscrepency(generics.ListAPIView):
    # permission_classes = (IsAuthenticated,)
    queryset = Discrepancy.objects.all()
    serializer_class = DiscrepencySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['property__id', 'room_occupancy__id', 'discrepancy_at']
    pagination_class = CustomSuccessPagination

from rest_framework import permissions
class TenantViewSet(ModelViewSet):
    """
    get or create or delete the tenant on user property
    properity owner can add user by email to this properity if the user registred
    he will find properity assigned to him
    if he not app user once he register this properity will assign to him
    """
    http_method_names = ['get', 'post', 'delete', 'head', 'options', 'trace']	
    serializer_class = TenantSerializer
    permission_classes = [permissions.IsAuthenticated]
    

    def get_property(self):
        properity_id = self.kwargs.get('pid')
        property = get_object_or_404(Property, id=properity_id, user=self.request.user)
        return property


    def get_queryset(self):
        return Tenant.objects.filter(property=self.get_property())

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['property'] = self.get_property()
        return context
        
    def perform_create(self, serializer):
        serializer.save(property = self.get_property())

from rest_framework.generics import RetrieveUpdateAPIView

class InspectionScheduleView(RetrieveUpdateAPIView):
    """
    inspection request schedule view set
    by passing property id in path
    """
    serializer_class = InspectionScheduleSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        property = get_object_or_404(
            Property, user= self.request.user,
            id=self.kwargs['id']
        )
        inspection_request= get_object_or_404(
            InspectionSchedule,
            property=property
        )
        return inspection_request