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
from semantic.models import SemanticEdge
from flags.models import Flag
from keywords.models import Keyword

from datetimewidget.widgets import DateTimeWidget
from django.forms.models import modelform_factory

#time
import datetime
from django.utils import timezone

from .forms import ArticleEditForm
from django.core.urlresolvers import reverse_lazy

#Save test
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect
import json
from semantic.serializers import SemanticNodeSerializer
from semantic.serializers import SemanticEdgeSerializer

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
    model = Article
    context_object_name = 'article_list'

    # def get_queryset(self):
        # slug = self.kwargs['slug']

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(SemanticView, self).get_context_data(**kwargs)

        # print(self.kwargs['slug'])
        # if 'slug' in self.request.POST:
        #     context['slug'] = self.kwargs['slug']

        if 'slug' in self.kwargs:
            # print("YES")

            article = Article.objects.get(slug=self.kwargs['slug'])
            # print(article.semantic_ids())
            # serializerArticle = ArticleEdgeSerializer(article)

            # context['article_semantic'] = serializerArticle.data["semantic"];
            context['selected_article'] = article
            context['article_nodes'] = json.dumps(article.semantic_ids())
            # context['slug'] = self.kwargs['slug']
        else:
            context['article_nodes'] = json.dumps([])

        context['title'] = 'Semantic'
        return context

def request_article_nodes(request):
    if request.method == 'POST':
        jsonData = json.loads(request.body.decode('utf-8'))
        articleId = jsonData["id"]

        article = Article.objects.get(pk=articleId);

        return HttpResponse(json.dumps({'message': article.semantic_ids()}))

    return HttpResponse(json.dumps({'message': []}))

def save_article_nodes(request):
    if request.method == 'POST':
        jsonData = json.loads(request.body.decode('utf-8'))
        articleId = jsonData["id"]
        articleNodes = jsonData["article_nodes"]

        article = Article.objects.get(pk = articleId)
        article.reset_semantic_ids(articleNodes)

        return HttpResponse(json.dumps({'message': 0}))

    return HttpResponse(json.dumps({'message': 1}))


def save_graph(request):
    if request.method == 'POST':
        jsonData = json.loads(request.body.decode('utf-8'))
        jsonNodes = jsonData["nodes"]
        jsonNodesClean = []
        jsonEdges = jsonData["edges"]
        jsonEdgesClean = []

        for node in jsonNodes:
            tmp = {}
            for attribute in node:
                if (attribute == "id") or (attribute == "name"):
                    tmp[attribute] = node[attribute]
            jsonNodesClean.append(tmp)

        for edge in jsonEdges:
            tmp = {}
            for attribute in edge:
                if (attribute == "id") or (attribute == "parent") or (attribute == "child"):
                    tmp[attribute] = edge[attribute]
            jsonEdgesClean.append(tmp)

        querysetNodes = Semantic.objects.all()
        querysetEdges = SemanticEdge.objects.all()

        serializerNodes = SemanticNodeSerializer(querysetNodes, data=jsonNodesClean, many=True)
        serializerEdges = SemanticEdgeSerializer(querysetEdges, data=jsonEdgesClean, many=True)

        # serializerNodes.is_valid()
        # serializerEdges.is_valid()
        # # print(serializerNodes.errors)
        # serializerNodes.validated_data
        # serializerEdges.validated_data
        if serializerNodes.is_valid():
            serializerNodes.save()
        # print(serializerNodes.errors)
        # print(serializerEdges.is_valid())
        # print(serializerEdges.errors)
        if serializerEdges.is_valid():
            serializerEdges.save()

    return HttpResponse(json.dumps({'message': 0}))

def add_edge(request):
    if request.method == 'POST':
        jsonData = json.loads(request.body.decode('utf-8'))

        edge = {}
        # print(jsonData)
        for attribute in jsonData:
            if (attribute == "id") or (attribute == "parent") or (attribute == "child"):
                edge[attribute] = jsonData[attribute]

        print("ODESLANO: ")
        print(edge)
        test = []
        test.append(edge)

        querysetEdges = SemanticEdge.objects.all()

        serializerEdges = SemanticEdgeSerializer(data=edge)

        if serializerEdges.is_valid():
            try:
                serializerEdges.save()
            except Exception as e:
                print(e)
                return HttpResponse(json.dumps({'message': 1}))

            print(serializerEdges.errors)
            return HttpResponse(json.dumps({'message': 0}))
        else:
            print(serializerEdges.errors)
            return HttpResponse(json.dumps({'message': 1}))



    # return HttpResponse("Got json data")


def login(request, template_name):
    login_context = {
        'title': 'Login',
    }
    template_response = views.login(request, template_name, extra_context=login_context)
    return template_response
