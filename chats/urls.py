from django.urls import path
from .views.chats import ChatsView, ChatView

urlpatterns = [
    path('', ChatsView.as_view()),
    path('<int:chat_id>/', ChatView.as_view()),
]