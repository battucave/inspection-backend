from django.core.exceptions import ValidationError
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated,AllowAny
from django.http import Http404
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Property,PropertyType,Room,PropertyApplication
from .serializers import  PropertySerializer,PropertyTypeSerializer,RoomSerializer,PropertyApplicationSerializer
from authapp.permissions import  IsOwner, IsOwnerOrReadOnly
from authapp.models import User
from rest_framework import filters 
from rest_framework.pagination import LimitOffsetPagination 
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action

class NewProperty(APIView):
    """Create,Update,Delete for single property"""
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
            raise Http404
   
    #@action(detail=False, methods=['post'], parser_classes=(FormParser, ))
    #@swagger_auto_schema(request_body=PropertySerializer)
    def post(self, request):
        serializer = PropertySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    

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
            raise Http404
    def get(self,request,pk):
        """Return single property"""
        emergency = self.get_object(pk)
        serializer = PropertySerializer(emergency)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    
    def put(self, request, pk, format=None):
        """Update property"""
        emergency = self.get_object(pk)
        serializer = PropertySerializer(emergency, data=request.data)
        print(serializer)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response({serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    
    def delete(self, request, pk, format=None):
        """Delete Property"""
        property = self.get_object(pk)
        if property.user == request.user:
            property.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

class PropertyTypeView(APIView):
    """Return all property types"""
    def get(self,request):
        property_types = PropertyType.objects.all()
        property_type_serializer = PropertyTypeSerializer(property_types, many=True)
        return Response(property_type_serializer.data)




class PropertySearchView(generics.ListAPIView):
    """Property search"""
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description','address']

class AllProperty(APIView, LimitOffsetPagination):
    """Return all properties"""
    def get(self,request):
        properties = Property.objects.all()
        results = self.paginate_queryset(properties, request, view=self)
        serializer = PropertySerializer(results, many=True)
        return self.get_paginated_response(serializer.data)
        

class UserProperty(APIView, LimitOffsetPagination):
    """Return properties of the logged in user"""
    permission_classes = (IsAuthenticated,)
    

    def get(self,request):
        properties = Property.objects.filter(user=request.user)
        results = self.paginate_queryset(properties, request, view=self)
        property_serializer = PropertySerializer(results, many=True)
        return Response(property_serializer.data)

class GetUserProperty(APIView):
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
        return Response(property_serializer.data)

    
class NewRoom(APIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = RoomSerializer
    

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise Http404
        
    def post(self, request,pk):
        try:
            property =Property.objects.get(pk=pk)
        except Property.DoesNotExist:
            raise Http404
        serializer = RoomSerializer(data=request.data)
        if property.user != request.user:
            raise Http404("You are not authorized to create a room in this property")
        if serializer.is_valid():
            serializer.save(property=property)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    


class RoomView(APIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = RoomSerializer
    

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise Http404
    def get(self,request,pk):
        room = self.get_object(pk)
        serializer = RoomSerializer(room)
        return Response(serializer.data,status=status.HTTP_200_OK)
        
   
    def put(self, request, pk, format=None):
        room = self.get_object(pk)
        if room.property.user != request.user:
            raise Http404("Not authorized")
        serializer = RoomSerializer(room, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    def delete(self, request, pk, format=None):
        room = self.get_object(pk)
        if room.property.user == request.user:
            room.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

class PropertyRooms(APIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = RoomSerializer

    def get_object(self, pk):
        try:
            return Property.objects.get(pk=pk)
        except Property.DoesNotExist:
            raise Http404
    def get(self,request,pk):
        property = self.get_object(pk)
        rooms = Room.objects.filter(property=property)
        serializer = RoomSerializer(rooms,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)


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
            raise Http404
        serializer = PropertyApplicationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(property=property, owner=property.user,tenant=request.user,state='pending')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PropertyApplicationUpdate(APIView):
    """Property application can only be updated by owner"""
    permission_classes = (IsAuthenticated,)
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = PropertyApplicationSerializer
    

    def get_object(self, pk):
        try:
            return Property.objects.get(pk=pk)
        except Property.DoesNotExist:
            raise Http404
        
    def put(self, request,pk):
        try:
            property =PropertyApplication.objects.get(pk=pk)
        except PropertyApplication.DoesNotExist:
            raise Http404
        if request.user != property.owner:
            raise Http404("You are not authorized to change this application")
        serializer = PropertyApplicationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class PropertyApplications(generics.ListAPIView):
    """List Property Applications """
    permission_classes = (IsAuthenticated,)
    queryset = PropertyApplication.objects.all()
    serializer_class = PropertyApplicationSerializer
    #filter_backends = [filters.SearchFilter]
    #search_fields = ['owner', 'tenant','state']
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['owner', 'tenant','state']