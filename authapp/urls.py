from django.urls import path,include
from . import views
urlpatterns = [
    path('',include('djoser.urls')),
    path('',include('djoser.urls.authtoken')),
    path('', include('djoser.urls.jwt')),
    path('owner/create',views.CreateOwner.as_view()),
    path('maintenance/create',views.CreateMaintenance.as_view()),
    path('vendor/create',views.CreateVendor.as_view()),
    path('user/delete/<str:pk>/',views.DeleteUser.as_view())
     
    
]