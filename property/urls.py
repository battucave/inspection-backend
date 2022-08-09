from django.urls import path
from property import views
urlpatterns = [

    path('property/',views.NewProperty.as_view()),
    path('propertytype/',views.PropertyTypeView.as_view()),

]
