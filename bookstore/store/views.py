from django.views.generic import TemplateView, RedirectView


class HomeView(TemplateView):
    template_name = 'index.html'


class RedirectToHomeView(RedirectView):
    pattern_name = 'home'
