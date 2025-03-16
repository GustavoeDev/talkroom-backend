from rest_framework.views import APIView

from django.db.models import Q
from django.utils.timezone import now

from users.models import User

from chats.models import Chat, Message
from chats.utils.exceptions import UserNotFound, ChatNotFound
from chats.serializers import ChatSerializer


class BaseView(APIView):
    def get_user(self, raise_exception=True, **kwargs) -> User | None:
        user = User.objects.filter(**kwargs).first()

        if not user and raise_exception:
            raise UserNotFound
        
        return user
    
    def chat_exists(self, user_id, to_user) -> Chat | None:
        chat = Chat.objects.filter(
            (Q(from_user=user_id) & Q(to_user=to_user)) |
            (Q(from_user=to_user) & Q(to_user=user_id)),
            deleted_at__isnull=True
        )

        if chat:
            return ChatSerializer(chat, context={'user_id': user_id}).data
        
    def chat_belongs_to_user(self, user_id, chat_id) -> Chat | None:
        chat = Chat.objects.filter(
            Q(from_user=user_id) | Q(to_user=user_id),
            id=chat_id,
            deleted_at__isnull=True
        ).first()

        if not chat:
            raise ChatNotFound
        
        return chat

    def mark_messages_as_read(self, chat_id, user_id) -> None:
        Message.objects.filter(
            chat_id=chat_id,
            viewed_at__isnull=True,
            deleted_at__isnull=True,
        ).exclude(
            from_user=user_id
        ).update(
            viewed_at=now()
        )