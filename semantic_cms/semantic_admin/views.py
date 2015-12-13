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
from django.views.generic.edit import DeleteView
from django.views.generic.edit import UpdateView
from django.views.generic import TemplateView
from django.views.generic import ListView
from django_filters.views import FilterView
from article.filter import ArticleFilter

from article.models import Article
from semantic.models import Semantic
from flags.models import Flag
from keywords.models import Keyword

from datetimewidget.widgets import DateTimeWidget
from django.forms.models import modelform_factory

#time
import datetime
from django.utils import timezone

from .forms import ArticleEditForm
from django.core.urlresolvers import reverse_lazy

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

class ModelFormWidgetMixin(object):
    def get_form_class(self):
        return modelform_factory(self.model, fields=self.fields, widgets=self.widgets)

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "semantic_admin/dashboard.html"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(DashboardView, self).get_context_data(**kwargs)
        context['title'] = 'Dashboard'
        return context

# class ContentView(LoginRequiredMixin, ListView):
#     template_name = "semantic_admin/content.html"
#     model = Article
#     context_object_name = 'article_list'
#
#     def get_context_data(self, **kwargs):
#         # Call the base implementation first to get a context
#         context = super(ContentView, self).get_context_data(**kwargs)
#
#         context['title'] = 'Dashboard'
#         return context

class ContentView(LoginRequiredMixin, FilterView):
    template_name = "semantic_admin/content.html"
    filterset_class = ArticleFilter
    context_object_name = 'article_list'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(ContentView, self).get_context_data(**kwargs)
        context['request'] = self.request
        context['title'] = 'Dashboard'
        return context

class CreateArticleView(LoginRequiredMixin, CreateView):
    template_name = "semantic_admin/edit_article.html"
    success_url = reverse_lazy('semantic_admin:content:index')
    form_class = ArticleEditForm

    def get_initial(self):
        initial = super(CreateArticleView, self).get_initial()
        initial["created_date"] = datetime.datetime.now()
        # initial["author"] = self.request.user
        return initial

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(CreateArticleView, self).get_context_data(**kwargs)
        context['title'] = 'Create New Article'
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user

        if self.request.POST:
            if 'publish' in self.request.POST:
                form.instance.publish_article(datetime.datetime.now())

        form.save()
        return super(CreateArticleView, self).form_valid(form)

class UpdateArticleView(LoginRequiredMixin, UpdateView):
    model = Article
    template_name = "semantic_admin/edit_article.html"
    success_url = reverse_lazy('semantic_admin:content:index')
    form_class = ArticleEditForm

class DeleteArticleView(LoginRequiredMixin, DeleteView):
    template_name = "semantic_admin/article_confirm_delete.html"
    model = Article
    success_url = reverse_lazy('semantic_admin:content:index')

class SemanticView(LoginRequiredMixin, ListView):
    template_name = "semantic_admin/semantic.html"
    model = Semantic
    context_object_name = 'dag_list'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(SemanticView, self).get_context_data(**kwargs)

        context['title'] = 'Semantic'
        return context


def login(request, template_name):
    login_context = {
        'title': 'Login',
    }
    template_response = views.login(request, template_name, extra_context=login_context)
    return template_response
