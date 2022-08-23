from django.urls import path
from . import views
urlpatterns = [
    path('request/create/<str:pk>/',views.RequestView.as_view()),
    path('request/<str:pk>/',views.GetRequestView.as_view()),
    path('requests/',views.ListRequestView.as_view()),
    
]
