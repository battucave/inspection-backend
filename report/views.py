from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.http import Http404
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from .serializers import ReportSerializer
from .models import Report
from authapp.models import User
from rest_framework import generics
from rest_framework import filters 
from django_filters.rest_framework import DjangoFilterBackend

class ReportView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = ReportSerializer
    permission_classes = (IsAuthenticated,)
    
    def get_object(self, pk):
        try:
            return Report.objects.get(pk=pk)
        except Report.DoesNotExist:
            raise Http404

    def post(self, request):
        serializer = ReportSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    


class GetReportView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = ReportSerializer
    permission_classes = (IsAuthenticated,)
    def get_object(self, pk):
        try:
            return Report.objects.get(pk=pk)
        except Report.DoesNotExist:
            raise Http404
    

    def get(self,request,pk):
        report = self.get_object(pk)
        serializer = ReportSerializer(report)
        return Response(serializer.data)
    
    def put(self, request, pk, format=None):
        report = self.get_object(pk)
        if request.user!=report.user:
            raise Http404
        serializer = ReportSerializer(report, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    def delete(self, request, pk, format=None):
        report = self.get_object(pk)
        if request.user == report.user:
            report.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)




class GetReportList(generics.ListAPIView):
    """Return all the reports of the current logged in user"""
    serializer_class = ReportSerializer
    filter_backends = [DjangoFilterBackend]

    def get_queryset(self):
        return Report.objects.filter(user=self.request.user)



class GetUserReportList(generics.ListAPIView):
    """Return all the reports of the user with the pk"""
    serializer_class = ReportSerializer
    filter_backends = [DjangoFilterBackend]
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        pk = self.kwargs['pk']
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

        return Report.objects.filter(user=user)


class ListReports(generics.ListAPIView):
    """Return all the reports"""
    serializer_class = ReportSerializer
    filter_backends = [DjangoFilterBackend]
    permission_classes = (IsAuthenticated,)
    queryset = Report.objects.all()