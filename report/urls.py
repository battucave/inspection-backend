from django.urls import path
from . import views
urlpatterns = [
    path('report/create/',views.ReportView.as_view()),


    path('report/<str:pk>/',views.GetReportView.as_view()),
    path('report/<str:pk>/',views.ReportView.as_view()),
    path('report/',views.ReportView.as_view()),
    
]
