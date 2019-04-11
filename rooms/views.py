from .models import Room, Message
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from koda.views import BaseView

class BaseRoomView(LoginRequiredMixin, BaseView):

    template_name = "rooms/base.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["rooms"] = self.request.user.room_set.all()
        return context

class DetailRoomView(BaseRoomView):

    template_name = "rooms/room.html"

    def dispatch(self, request, *args, **kwargs):
        self.room = get_object_or_404(Room, pk=kwargs["room_id"])
        if request.user not in self.room.members:
            raise PermissionDenied
        return super(DetailRoomView, self).dispatch(
            request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["room_id"] = kwargs["room_id"]
        context["room_name"] = self.room.name
        context["username"] = self.request.user.username
        return context
