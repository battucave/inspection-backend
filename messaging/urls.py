from django.urls import path
from . import views
urlpatterns = [
    path('message/new/<str:pk>/',views.NewMessage.as_view()),
    path('messages/<str:pk>/',views.MessageListView.as_view()),
    path('conversations/', views.ConversationsListView.as_view())
  

]
