from django.urls import path
from property import views
urlpatterns = [
     path('property/all/',views.AllProperty.as_view()),
path('property/search/',views.PropertySearchView.as_view()),
    path('property/',views.NewProperty.as_view()),
    path('property/<str:pk>/',views.NewProperty.as_view()),
    path('propertytype/',views.PropertyTypeView.as_view()),

]
