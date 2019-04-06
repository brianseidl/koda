from .models import Channel, Message
from django.contrib.auth.models import User
from django.views.generic.base import TemplateView

class BaseView(TemplateView):

    template_name = "communications/base.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
