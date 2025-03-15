from rest_framework import serializers

from users.serializers import UserSerializer

from .models import Chat, Message

from attachments.models import FileAttachment, AudioAttachment
from attachments.serializers import FileAttachmentSerializer, AudioAttachmentSerializer


class ChatSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    message_not_viewed = serializers.SerializerMethodField()
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = Chat
        fields = ['id', 'user', 'message_not_viewed', 'last_message', 'viewed_at', 'created_at']

    def get_user(self, chat):
        user = chat.from_user

        if user.id == self.context['user_id']:
            user = chat.to_user
        
        return UserSerializer(user).data
    
    def get_message_not_viewed(self, chat):
        message_not_viewed = Message.objects.filter(
            chat_id=chat.id,
            viewed_at__isnull=True,
            deleted_at__isnull=True,
        ).exclude(from_user=self.context['user_id']).count()

        return message_not_viewed

    def get_last_message(self, chat):
        last_message = Message.objects.filter(
            chat_id=chat.id,
            deleted_at__isnull=True,
        ).order_by('-created_at').first()

        if not last_message:
            return None
        
        return MessageSerializer(last_message).data


class MessageSerializer(serializers.ModelSerializer):
    from_user = serializers.SerializerMethodField()
    attachment = serializers.SerializerMethodField()
        
    class Meta:
        model = Message
        fields = ['id', 'body', 'attachment', 'from_user', 'viewed_at', 'created_at']

    def get_from_user(self, message):
        return UserSerializer(message.from_user).data
    
    def get_attachment(self, message):
        if message.attachment_cody == 'FILE':
            file_attachment = FileAttachment.objects.filter(
                id=message.attachment_id
            ).first()

            if not file_attachment:
                return None
            
            return {
                'file': FileAttachmentSerializer(file_attachment).data,
            }
        
        if message.attachment_cody == 'AUDIO':
            audio_attachment = AudioAttachment.objects.filter(
                id=message.attachment_id
            ).first()

            if not audio_attachment:
                return None
            
            return {
                'audio': AudioAttachmentSerializer(audio_attachment).data,
            }