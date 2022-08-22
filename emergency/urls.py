from django.urls import path
from . import views
urlpatterns = [
   path('contacts/',views.ListUserEmergency.as_view()),
    path('contact/create/',views.NewEmergencyView.as_view()),
    path('contact/',views.ListUserEmergency.as_view()),
    path('contact/<str:pk>/',views.GetEmergencyView.as_view()),
   
  

]
