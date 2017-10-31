from django.shortcuts import render
from django.views.generic import TemplateView
from auth.auth import log_required


class IndexView(TemplateView):

    template_name = 'posts/posts_index.html'

    @log_required
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, { })
