from rest_framework.views import APIView
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

from inspection.permissions import CustomIsAuthenticatedPerm as IsAuthenticated
from inspection.pagination import CustomSuccessPagination
class ReportView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = ReportSerializer
    permission_classes = (IsAuthenticated,)
    
    def get_object(self, pk):
        try:
            return Report.objects.get(pk=pk)
        except Report.DoesNotExist:
            return Response({'success':False,'error':True,'msg':'Report not found','data':{}},status=status.HTTP_200_OK)


    def post(self, request):
        serializer = ReportSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({'success':True,'error':False,'msg':'Report created','data':serializer.data},status=status.HTTP_201_CREATED)
    
        return Response({'success':False,'error':True,'msg':'Error creating Report','data':serializer.errors},status=status.HTTP_200_OK)

    


class GetReportView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = ReportSerializer
    permission_classes = (IsAuthenticated,)
    def get_object(self, pk):
        try:
            return Report.objects.get(pk=pk)
        except Report.DoesNotExist:
            return Response({'success':False,'error':True,'msg':'Report not found','data':{}},status=status.HTTP_200_OK)

    

    def get(self,request,pk):
        report = self.get_object(pk)
        serializer = ReportSerializer(report)
        return Response({'success':True,'error':False,'msg':'Request created','data':serializer.data},status=status.HTTP_201_CREATED)
    
    
    def put(self, request, pk, format=None):
        report = self.get_object(pk)
        if request.user!=report.user:
            raise Http404
        serializer = ReportSerializer(report, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'success':True,'error':False,'msg':'','data':serializer.data},status=status.HTTP_200_OK)
        return Response({'success':False,'error':True,'msg':'Request failed','data':serializer.data},status=status.HTTP_200_OK)
    
    
    def delete(self, request, pk, format=None):
        report = self.get_object(pk)
        if request.user == report.user:
            report.delete()
            return Response({'success':True,'error':False,'msg':'','data':{}},status=status.HTTP_200_OK)
    
        return Response({'success':False,'error':True,'msg':'Operation failed','data':{}},status=status.HTTP_200_OK)
    



class GetReportList(generics.ListAPIView):
    """Return all the reports of the current logged in user"""
    serializer_class = ReportSerializer
    filter_backends = [DjangoFilterBackend]
    pagination_class = CustomSuccessPagination

    def get_queryset(self):
        return Report.objects.filter(user=self.request.user)



class GetUserReportList(generics.ListAPIView):
    """Return all the reports of the user with the pk"""
    serializer_class = ReportSerializer
    filter_backends = [DjangoFilterBackend]
    permission_classes = (IsAuthenticated,)
    pagination_class = CustomSuccessPagination

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
    pagination_class = CustomSuccessPagination