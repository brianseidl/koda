from .models import Room, Message
from django.contrib.auth.models import User
from django.views.generic.base import TemplateView

class BaseRoomView(TemplateView):

    template_name = "rooms/base.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["rooms"] = self.request.user.room_set.all()
        return context

class DetailRoomView(BaseRoomView):

    template_name = "rooms/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        room = Room.objects.get(id=kwargs["room_id"])
        context["room_name"] = room.name
        return context
