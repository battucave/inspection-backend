from django.shortcuts import render
from rest_framework.views import APIView
from .models import Conversation
from django.db.models import Q
from rest_framework.pagination import LimitOffsetPagination 
from .serializers import ConversationSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status


class ConversationList(APIView):
   def get(self,request):
        a=''
        b=''
        conversation = Conversation.objects.filter(Q(user_one=a)|Q(user_two=b)) 

        conversation = Conversation.objects.filter(Q(user_one=b,user_two=a)|Q(user_one=a,user_two=b)) 



class ConversationListView(APIView, LimitOffsetPagination):
    """Return list of conversations this user is user is engaged in ordered by last massage time"""
    def get(self,request,pk):
        conversations = Conversation.objects.filter(Q(user_one=request.user)|Q(user_two=request.user)) 
        results = self.paginate_queryset(conversations, request, view=self)
        serializer = ConversationSerializer(results, many=True)
        return self.get_paginated_response(serializer.data)

class MessageListView(APIView, LimitOffsetPagination):
    """Return list of messages between two users"""
    def get(self,request,pk):
        conversations = Conversation.objects.filter(Q(user_one=request.user)|Q(user_two=request.user)) 
        results = self.paginate_queryset(conversations, request, view=self)
        serializer = ConversationSerializer(results, many=True)
        return self.get_paginated_response(serializer.data)


class NewMessage(APIView):
    """Create a new message"""
    permission_classes = (IsAuthenticated,)
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = RoomSerializer
    

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise Http404
        
    def post(self, request,pk):
        try:
            property =Property.objects.get(pk=pk)
        except Property.DoesNotExist:
            raise Http404
        serializer = RoomSerializer(data=request.data)
        if property.user != request.user:
            raise Http404("You are not authorized to create a room in this property")
        if serializer.is_valid():
            serializer.save(property=property)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
