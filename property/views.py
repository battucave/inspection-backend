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
from .models import Property,PropertyType,Room
from .serializers import  PropertySerializer,PropertyTypeSerializer,RoomSerializer
from authapp.permissions import  IsOwner, IsOwnerOrReadOnly
from authapp.models import User
from rest_framework import filters       
class NewProperty(APIView):
    permission_classes = (IsOwnerOrReadOnly,)
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = PropertySerializer
    
    

    #def perform_create(self, serializer):
    #    obj = serializer.save()
    #    for f in self.request.data.getlist('files'):
    #        mf = MyFile.objects.create(file=f)
    #        obj.files.add(mf)

    def get_object(self, pk):
        try:
            return Property.objects.get(pk=pk)
        except Property.DoesNotExist:
            raise Http404
    def get(self,request,pk):
        emergency = self.get_object(pk)
        serializer = PropertySerializer(emergency)
        return Response(serializer.data,status=status.HTTP_200_OK)
        
    def post(self, request):
        serializer = PropertySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk, format=None):
        emergency = self.get_object(pk)
        serializer = PropertySerializer(emergency, data=request.data)
        print(serializer)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    def delete(self, request, pk, format=None):
        property = self.get_object(pk)
        if property.user == request.user:
            property.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

class PropertyTypeView(APIView):
    def get(self,request):
        property_types = PropertyType.objects.all()
        property_type_serializer = PropertyTypeSerializer(property_types, many=True)
        return Response(property_type_serializer.data)




class PropertySearchView(generics.ListAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description','address']

class AllProperty(APIView):
    """Return all properties"""
    def get(self,request):
        
        result = Property.objects.all()
        property_serializer = PropertySerializer(result, many=True)
        return Response(property_serializer.data)

class UserProperty(APIView):
    """Return properties of the logged in user"""
    permission_classes = (IsAuthenticated,)
    

    def get(self,request):
        result = Property.objects.filter(user=request.user)
        property_serializer = PropertySerializer(result, many=True)
        return Response(property_serializer.data)

class GetUserProperty(APIView):
    """Return properties of the user with the pk"""
    permission_classes = (IsAuthenticated,)
    

    def get(self,request,pk):
        try:
            user = User.objects.get(pk=pk)
        except:
            user = None

        result = Property.objects.filter(user=user)
        property_serializer = PropertySerializer(result, many=True)
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
            raise Http404
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
            return Response(serializer.data)
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