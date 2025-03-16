from django.urls import path
from .views.chats import ChatsView, ChatView
from .views.messages import MessagesView, MessageView

urlpatterns = [
    path('', ChatsView.as_view()),
    path('<int:chat_id>/', ChatView.as_view()),
    path('<int:chat_id>/messages/', MessagesView.as_view()),
    path('<int:chat_id>/messages/<int:message_id>/', MessageView.as_view()),
]