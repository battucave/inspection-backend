from django.urls import path
from . import views
urlpatterns = [

    path('contact/<str:pk>/',views.EmergencyView.as_view()),
    path('contact/',views.GetEmergencyView.as_view()),
    path('contact/',views.EmergencyView.as_view()),

]
