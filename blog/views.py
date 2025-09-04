from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = 'home.html'

class PostView(TemplateView):
    template_name = 'post.html'

