from django.urls import path,include
from . import views




#    path('',include('djoser.urls.authtoken')),

urlpatterns = [
   
path('',include('djoser.urls')),
    path('profilepicture/',views.UploadUserImage.as_view()),
    path('user/create/',views.CreateUser.as_view()),
    path('user/delete/<str:pk>/',views.DeleteUser.as_view()),
     path('getuser/<str:pk>/',views.GetSingleUser.as_view()),
  
      path('login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', views.TokenRefreshView.as_view(), name='token_refresh'),
    path('verification/check/',views.VerifyCode.as_view(),name='verify_code'),
    path('verification/refresh/',views.RefreshVerifyCode.as_view(),name='refresh_verify_code'),
    
    
     
    
]

#path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
          