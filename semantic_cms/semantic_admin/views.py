# from django.shortcuts import render

# from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
# from django.http import HttpResponse
# import datetime

from django.contrib.auth import views
# from django.template.response import TemplateResponse
# from django.template import RequestContext

from django.views.generic.edit import CreateView
from django.views.generic import TemplateView
from django.views.generic import ListView

from article.models import Article
from semantic.models import Semantic
from flags.models import Flag
from keywords.models import Keyword
# @login_required
# def dashboard(request):
#     now = datetime.datetime.now()
#     html = "<html><body>It is now %s.</body></html>" % now
#     return HttpResponse(html)

class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "semantic_admin/dashboard.html"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(DashboardView, self).get_context_data(**kwargs)

        context['title'] = 'Dashboard'
        return context

class ContentView(LoginRequiredMixin, ListView):
    template_name = "semantic_admin/content.html"
    model = Article
    context_object_name = 'article_list'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(ContentView, self).get_context_data(**kwargs)

        context['title'] = 'Dashboard'
        return context

class CreateArticleView(LoginRequiredMixin, CreateView):
    template_name = "semantic_admin/create_article.html"
    model = Article
    fields = ["title"]

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(CreateArticleView, self).get_context_data(**kwargs)

        context['title'] = 'Create New Article'
        return context

def login(request, template_name):
    login_context = {
        'title': 'Login',
    }
    template_response = views.login(request, template_name, extra_context=login_context)
    return template_response
