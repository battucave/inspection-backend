from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.http import Http404
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from .serializers import MRequestSerializer
from .models import MRequest

class RequestView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = MRequestSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = []


    def get_object(self, pk):
        try:
            return MRequest.objects.get(pk=pk)
        except MRequest.DoesNotExist:
            raise Http404

    def post(self, request):
        serializer = MRequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format=None):
        report = self.get_object(pk)
        serializer = MRequestSerializer(report, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    #TODO check if request user is the MRequest user
    def delete(self, request, pk, format=None):
        report = self.get_object(pk)
        report.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class GetRequestView(APIView):
    queryset = MRequest.objects.all()
    serializer_class = MRequestSerializer
    authentication_classes = []

    def get_object(self, pk):
        try:
            return MRequest.objects.get(pk=pk)
        except MRequest.DoesNotExist:
            raise Http404
    

    def get(self,request,pk):
        report = self.get_object(pk)
        serializer = MRequestSerializer(report)
        return Response(serializer.data)
    
    