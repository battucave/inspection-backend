from django.urls import path
from . import views
urlpatterns = [
    path('request/create/',views.RequestView.as_view()),


    path('request/<str:pk>/',views.GetRequestView.as_view()),
    path('request/<str:pk>/',views.RequestView.as_view()),
    path('request/',views.RequestView.as_view()),
    
]
