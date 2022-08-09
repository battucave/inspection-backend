from django.urls import path,include
from . import views
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

urlpatterns = [
    path('',include('djoser.urls')),
    path('',include('djoser.urls.authtoken')),
    path('', include('djoser.urls.jwt')),
    path('owner/create',views.CreateOwner.as_view()),
    path('maintenance/create',views.CreateMaintenance.as_view()),
    path('vendor/create',views.CreateVendor.as_view()),
    path('user/delete/<str:pk>/',views.DeleteUser.as_view()),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    
     
    
]

#path('verification/refresh')
#    path('verification/check')