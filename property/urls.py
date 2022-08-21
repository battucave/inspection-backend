from django.urls import path
from property import views
urlpatterns = [
    path('property/all/',views.AllProperty.as_view()),
    path('property/create/',views.NewProperty.as_view()),
     path('property/<str:pk>/',views.GetProperty.as_view()),
    path('property/',views.PropertySearchView.as_view()),
   
    path('property/<str:pk>/rooms/',views.PropertyRooms.as_view()),
    path('propertytype/',views.PropertyTypeView.as_view()),
    path('property/<str:pk>/room/create/',views.NewRoom.as_view()),
    path('room/<str:pk>/',views.RoomView.as_view()),
    path('user/property/', views.UserProperty.as_view()),
    path('user/<str:pk>/property/', views.GetUserProperty.as_view()),
    path('property/<str:pk>/apply/', views.NewPropertyApplication.as_view()),
    path('application/<str:pk>/', views.PropertyApplicationUpdate.as_view()), 
    path('applications/', views. PropertyApplications.as_view()), 
 
]
