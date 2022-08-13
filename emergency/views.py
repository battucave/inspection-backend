from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.http import Http404
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from .serializers import EmergencySerializer
from .models import Emergency

class EmergencyView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = EmergencySerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = []

    #def perform_create(self, serializer):
    #    obj = serializer.save()
    #    for f in self.request.data.getlist('files'):
    #        mf = MyFile.objects.create(file=f)
    #        obj.files.add(mf)

    def get_object(self, pk):
        try:
            return Emergency.objects.get(pk=pk)
        except Emergency.DoesNotExist:
            raise Http404

    def post(self, request):
        serializer = EmergencySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format=None):
        emergency = self.get_object(pk)
        serializer = EmergencySerializer(emergency, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    #TODO check if request user is the emergency user
    def delete(self, request, pk, format=None):
        emergency = self.get_object(pk)
        emergency.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class GetEmergencyView(APIView):
    queryset = Emergency.objects.all()
    serializer_class = EmergencySerializer
    authentication_classes = []

    def get_object(self, pk):
        try:
            return Emergency.objects.get(pk=pk)
        except Emergency.DoesNotExist:
            raise Http404
    

    def get(self,request,pk):
        emergency = self.get_object(pk)
        serializer = EmergencySerializer(emergency)
        return Response(serializer.data)
    
    