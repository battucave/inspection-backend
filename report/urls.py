from django.urls import path
from . import views
urlpatterns = [
    path('report/create/',views.ReportView.as_view()),


    path('report/<str:pk>/',views.GetReportView.as_view()),
    path('reports/',views.GetReportList.as_view())
    
    
]

#path('<str:pk>/reports/',views.GetReportList.as_view())
    