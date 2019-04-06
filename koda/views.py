from django.views.generic.base import TemplateView

class BaseView(TemplateView):

    template_name = "koda/base.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
