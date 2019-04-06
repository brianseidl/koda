from django.urls import include, path
from .views import BaseView, DetailView

urlpatterns = [
    path('', BaseView.as_view(), name='index'),
    path('<int:channel_id>/', DetailView.as_view(), name='detail'),
]
