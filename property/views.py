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
from .models import Property,PropertyType
from .serializers import  PropertySerializer,PropertyTypeSerializer
from authapp.permissions import  IsOwner, IsOwnerOrReadOnly
        
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


class PropertySearchView(APIView):
    def get(self,request,q=""):
        print(q)
        result = Property.objects.filter(name__contains=q)
        property_serializer = PropertySerializer(result, many=True)
        return Response(property_serializer.data)


class AllProperty(APIView):
    def get(self,request,q=""):
        result = Property.objects.all()
        property_serializer = PropertySerializer(result, many=True)
        return Response(property_serializer.data)

class UserProperty(APIView):
    permission_classes = (IsAuthenticated,)
    

    def get(self,request):
        result = Property.objects.filter(user=request.user)
        property_serializer = PropertySerializer(result, many=True)
        return Response(property_serializer.data)