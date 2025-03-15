from django.contrib import admin
from .models import Chat, Message

@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ('id', 'from_user', 'to_user', 'viewed_at', 'deleted_at', 'created_at')

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'body', 'attachment_cody', 'attachment_id', 'viewed_at', 'deleted_at', 'created_at', 'chat', 'from_user')