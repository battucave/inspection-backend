from django.urls import path,include
from . import views



#    path('',include('djoser.urls.authtoken')),

urlpatterns = [
   
    path('',include('djoser.urls')),
    path("social-auth/", include('authapp.social-auth.urls')),

    path('profilepicture/',views.UploadUserImage.as_view()),
    path('user/create/',views.CreateUser.as_view()),
    path('user/update/',views.UpdateUser.as_view()),
    path('user/firebase/verify/',views.VerifyFirebaseUser.as_view()),
    path('user/delete/<str:pk>/',views.DeleteUser.as_view()),
    path('getuser/<str:pk>/',views.GetSingleUser.as_view()),
    path('login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', views.TokenRefreshView.as_view(), name='token_refresh'),
    path('verification/check/',views.VerifyCode.as_view(),name='verify_code'),
    path('verification/refresh/',views.RefreshVerifyCode.as_view(),name='refresh_verify_code'),
    path('password/reset/', views.PasswordResetView.as_view(), name='api-rest_password'),
    path('password/reset/confirm/', views.PasswordResetConfirmView.as_view(),
         name='api-rest_password_confirm'),
    path('password/reset/verify-token/',
         views.ResetPasswordVerifyToken.as_view(), name='api-rest_password'),
    
     
    
]

#path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
          