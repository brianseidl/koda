from django.views.generic.base import TemplateView
from django.contrib.auth.models import User

class BaseView(TemplateView):

    template_name = "koda/base.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        context["auth_user"] = isinstance(context["user"], User)
        return context
