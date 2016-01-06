__author__ = 'nolan'


from django.views.generic import TemplateView


class HomePageView(TemplateView):

    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        # context.update(self.get_data())
        return context

    def get_data(self):
        pass

