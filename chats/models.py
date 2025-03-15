from django import db
from django.db import models
from users.models import User

ATTACHMENT_CODY_CHOICES = [
    ('FILE', 'FILE'),
    ('AUDIO', 'AUDIO'),
]

class Chat(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_from_user')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_to_user')
    viewed_at = models.DateTimeField(null=True)
    deleted_at = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'chats'

    
class Message(models.Model):
    body = models.TextField(null=True)
    attachment_cody = models.CharField(choices=ATTACHMENT_CODY_CHOICES, max_length=15, null=True)
    attachment_id = models.IntegerField(null=True)
    viewed_at = models.DateTimeField(null=True)
    deleted_at = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    from_user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'chat_messages'