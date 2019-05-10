from .models import Room, Message
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView
from django.template.defaulttags import register
from koda.views import BaseView


class BaseView(TemplateView):

    template_name = "rooms/base.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        context["auth_user"] = isinstance(context["user"], User)
        return context


class BaseRoomView(LoginRequiredMixin, BaseView):

    template_name = "rooms/base_room.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_rooms = self.request.user.room_set.all()
        context["rooms"] = list(filter(lambda x: x.rtype == "room", all_rooms))
        context["type"] = "room"
        return context


class DetailRoomView(BaseRoomView):

    template_name = "rooms/detail_room.html"

    def dispatch(self, request, *args, **kwargs):
        self.room = get_object_or_404(Room, pk=kwargs["room_id"])
        if request.user not in self.room.members or self.room.rtype != "room":
            raise PermissionDenied
        return super(DetailRoomView, self).dispatch(
            request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["room_id"] = kwargs["room_id"]
        context["room_name"] = self.room.name
        context["username"] = self.request.user.username
        context["online_users"], context["offline_users"] = self.room.who_is_online()
        return context


class BaseChatView(LoginRequiredMixin, BaseView):

    template_name = "rooms/base_room.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_rooms = self.request.user.room_set.all()
        context["rooms"] = list(filter(lambda x: x.rtype == "chat", all_rooms))
        context["type"] = "chat"
        return context

    @register.filter
    def get_other_member(room, user):
        """
        View method to return the other member of the room.

        Args:
            room (Room): room in which you want to find the other user

        Returns:
            User: other member of the room that is not the user
                who sent the request.
        """
        return list(filter(lambda x: x != user, room.members))[0]


class DetailChatView(BaseChatView):

    template_name = "rooms/detail_room.html"

    def dispatch(self, request, *args, **kwargs):
        self.room = get_object_or_404(Room, pk=kwargs["chat_id"])
        if (request.user not in self.room.members) or (self.room.rtype != "chat"):
            raise PermissionDenied
        return super(DetailChatView, self).dispatch(
            request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["room_id"] = kwargs["chat_id"]
        context["room_name"] = self.room.name
        context["username"] = self.request.user.username
        context["online_users"], context["offline_users"] = self.room.who_is_online()
        return context
