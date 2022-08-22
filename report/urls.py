from django.urls import path
from . import views
urlpatterns = [
    path('report/create/',views.ReportView.as_view()),
    path('report/<str:pk>/',views.GetReportView.as_view()),
    path('reports/',views.ListReports.as_view()),
    path('user/reports/<str:pk>/',views.GetUserReportList.as_view())
    
    
]

#path