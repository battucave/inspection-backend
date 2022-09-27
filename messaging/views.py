from collections import OrderedDict

from django.shortcuts import render
from rest_framework.views import APIView
from .models import ConversationsModel,MessageModel, UploadedFile
from django.db.models import Q
from rest_framework.pagination import LimitOffsetPagination 
from rest_framework.parsers import MultiPartParser, FormParser
#from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework import pagination
from authapp.models import User
from django.http import Http404
from rest_framework.response import Response
from django.utils import timezone

from .serializers import serialize_dialog_model,serialize_message_model
from authapp.permissions import CustomIsAuthenticatedPerm as IsAuthenticated


class CustomSuccessPagination(LimitOffsetPagination):
    def get_paginated_response(self, data):
        datum = OrderedDict([
            ('count', self.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ])
        return Response({"success":True,"error":False,"msg":"","data":datum})



class MessageListView(APIView, CustomSuccessPagination):
    """Return list of conversations this user is user is engaged in ordered by last massage time"""
    def get_messages(self,user_two):
        
        qs = MessageModel.objects \
            .filter(Q(recipient=self.request.user, sender=user_two) |
                    Q(sender=self.request.user, recipient=user_two)) \
            .select_related('sender', 'recipient')
        #else:
        #    qs = MessageModel.objects.filter(Q(recipient=self.request.user) |
        #                                     Q(sender=self.request.user)).prefetch_related('sender', 'recipient', 'file')

        return qs.order_by('-created')
    def get(self,request,pk):
        try:
            user_two=User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({"success":False,"error":True,"msg":"User doesnot exist"},status=status.HTTP_200_OK)
        msgs = self.get_messages(user_two)
        results = self.paginate_queryset(msgs, request, view=self)
        data = [serialize_message_model(i, pk) for i in results]
        return self.get_paginated_response(data)

class ConversationsListView(APIView, CustomSuccessPagination):
    
    """Return list of conversations for the request user"""
    permission_classes = (IsAuthenticated,)
    def get(self,request):
        conversations = ConversationsModel.get_dialogs_for_user(request.user)
        results = self.paginate_queryset(conversations, request, view=self)
        serializer = [serialize_dialog_model(i,request.user.pk) for i in results]
        return self.get_paginated_response(serializer)

class NewConversation(APIView):
    permission_classes = (IsAuthenticated,)
    
    def post(self, request, pk):
        try:
            recipient = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({"success":False,"error":True,"msg":"User not found"},status=status.HTTP_200_OK)
        
        ConversationsModel.create_if_not_exists(request.user, recipient)
        #update the modified time of this Conversation
        dialog1 = ConversationsModel.objects.get(user_one=request.user,user_two=recipient)
        dialog1.modified=timezone.now()
        dialog1.save()

        seriliazer = serialize_dialog_model(dialog1, request.user.pk)

        return Response({"success":True,"error":False,"msg":"Conversation Created","data":seriliazer.data},status=status.HTTP_201_CREATED)

class NewMessage(APIView):
    """Create a new message"""
    permission_classes = (IsAuthenticated,)
    parser_classes = [MultiPartParser, FormParser]
    
        
    def post(self, request,pk):
        try:
            recipient =User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({"success":False,"error":True,"msg":"User not found"},status=status.HTTP_200_OK)
        text = request.data.get('text')
        file_obj = request.data.get('image')
        if file_obj:
            file_ = UploadedFile(file=file_obj,uploaded_by=request.user)
            file_.save()
        else:
            file_=None
        
        msg = MessageModel(sender=request.user,recipient=recipient,text=text)
        msg.save()
        if file_:
            msg.image = file_
            msg.save()
        

        return Response({"success":True,"error":False,"msg":"Message sent"},status=status.HTTP_201_CREATED)
        
    
    
    
