from django.urls import include, path
from .views import BaseView

urlpatterns = [
    path('', BaseView.as_view(), name='index'),
    path('channels/', include('communications.channels.urls')),
]
