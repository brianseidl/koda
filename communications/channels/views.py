from django.views.generic.base import TemplateView
from communications.models import Channel, Message

class BaseView(TemplateView):

    template_name = "channels/base.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["channels"] = self.request.user.channel_set.all()
        return context

class DetailView(TemplateView):

    template_name = "channels/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["channel_id"] = kwargs["channel_id"]
        channel = Channel.objects.get(id=context["channel_id"])
        context["channel_name"] = channel.name

        return context
