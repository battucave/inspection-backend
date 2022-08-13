from django.core.exceptions import ValidationError
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.http import Http404
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Property,PropertyType
from .serializers import  PropertySerializer,PropertyTypeSerializer

class NewProperty(APIView):
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = PropertySerializer
    permission_classes = (IsAuthenticated,)
    

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
    
    #TODO check if request user is the emergency user
    def delete(self, request, pk, format=None):
        emergency = self.get_object(pk)
        emergency.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class PropertyTypeView(APIView):
    queryset = PropertyType.objects.all()
    serializer_class = PropertyTypeSerializer
    authentication_classes = []
    

    def get(self,request):
        property_types = PropertyType.objects.all()
        property_type_serializer = PropertyTypeSerializer(property_types, many=True)
        return Response(property_type_serializer.data)
