from django.urls import include, path
from .views import *

app_name='rooms'

urlpatterns = [
    path('', BaseView.as_view(), name='homepage'),
    path('rooms/', BaseRoomView.as_view(), name='base_room'),
    path('chats/', BaseChatView.as_view(), name='base_chat'),
    path('rooms/<int:room_id>/', DetailRoomView.as_view(), name='detail_room'),
    path('chats/<int:chat_id>/', DetailChatView.as_view(), name='detail_chat'),
]
