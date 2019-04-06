from django.urls import include, path
from .views import BaseRoomView, DetailRoomView
app_name='rooms'
urlpatterns = [
    path('', BaseRoomView.as_view(), name='index'),
    path('<int:room_id>/', DetailRoomView.as_view(), name='detail'),
]
