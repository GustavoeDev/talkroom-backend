from rest_framework.response import Response

from django.db.models import Q
from django.utils.timezone import now

from chats.views.base import BaseView
from chats.models import Chat, Message
from chats.serializers import ChatSerializer

from core.socket import socket


class ChatsView(BaseView):
    def get(self, request):
        chats = Chat.objects.filter(
            Q(from_user_id=request.user.id) | Q(to_user_id=request.user.id),
            deleted_at__isnull=True
        ).order_by('-viewed_at').all()

        serializer = ChatSerializer(
            chats, 
            context={'user_id': request.user.id}, 
            many=True
        )

        return Response({
            'chats': serializer.data
        })
    
    def post(self, request):
        email = request.data.get('email')

        to_user = self.get_user(email=email)

        if to_user == request.user:
            return Response({
                'error': 'Não pode criar um chat com você mesmo'
            })

        chat = self.chat_exists(user_id=request.user.id, to_user=to_user.id)

        if not chat:
            chat = Chat.objects.create(
                from_user=request.user,
                to_user=to_user,
                viewed_at=now()
            )

            chat = ChatSerializer(chat, context={'user_id': request.user.id}).data

            socket.emit('update_chats', {
                'query': {
                    'users': [
                        request.user.id, 
                        to_user.id
                    ]
                }
            })

        return Response({
            'chat': chat
        })
    

class ChatView(BaseView):
    def delete(self, request, chat_id):
        chat = self.chat_belongs_to_user(
            user_id=request.user.id, 
            chat_id=chat_id
        )

        deleted_chat = Chat.objects.filter(
            id=chat_id,
            deleted_at__isnull=True
        ).update(
            deleted_at=now()
        )

        if deleted_chat:
            socket.emit('update_chats', {
                'type': 'delete',
                'query': {
                    'chat_id': chat_id,
                    'users': [
                        chat.from_user_id,
                        chat.to_user_id
                    ]
                }
            })

        return Response({
            'success': True
        })
            