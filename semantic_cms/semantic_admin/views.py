from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from django.contrib.auth import views

from django.views.generic.edit import CreateView
from django.views.generic.edit import DeleteView
from django.views.generic.edit import UpdateView
from django.views.generic import TemplateView
from django.views.generic import ListView
from django_filters.views import FilterView
from article.filter import ArticleFilter, ArticleFilterSemantic

from article.models import Article
from semantic.models import Semantic
from semantic.models import SemanticEdge
from flags.models import Flag
from keywords.models import Keyword
from .models import UserProfile
from .models import BlogSettings

from datetimewidget.widgets import DateTimeWidget
from django.forms.models import modelform_factory

from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger

#time
import datetime
from django.utils import timezone

from .forms import ArticleEditForm
from .forms import ArticleFlagEditForm
from .forms import UserProfileEditForm
from django.core.urlresolvers import reverse_lazy

#Save test
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect
import json
from semantic.serializers import SemanticNodeSerializer
from semantic.serializers import SemanticEdgeSerializer

from django.contrib.auth.models import User
from django.utils.text import slugify

# from settings import BASE_DIR


class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(LoginRequiredMixin, self).get_context_data(**kwargs)
        context['user_profile'] = UserProfile.objects.filter(user = self.request.user)
        return context

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

class CreateArticleFlagView(LoginRequiredMixin, CreateView):
    template_name = "semantic_admin/article_flag_edit.html"
    success_url = reverse_lazy('admin:article_types:index')
    form_class = ArticleFlagEditForm

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(CreateArticleFlagView, self).get_context_data(**kwargs)
        context['article_flags'] = Flag.objects.all()
        context['title'] = 'Create New Article Type'
        context['button_text'] = "Add new"
        return context

class UpdateUserProfileView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = "semantic_admin/user_profile_edit.html"
    success_url = reverse_lazy('admin:settings:user:index')
    form_class = UserProfileEditForm

    def get_form_kwargs(self):
        kwargs = super(UpdateUserProfileView, self).get_form_kwargs()
        kwargs.update(instance={
            'info': self.object,
            'user': self.object.user,
        })
        return kwargs

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(UpdateUserProfileView, self).get_context_data(**kwargs)
        context['title'] = 'Edit User Info'
        context['user_profile'] = UserProfile.objects.filter(user = self.request.user)
        return context

    def get_object(self):
        obj, created = UserProfile.objects.get_or_create(user = self.request.user)
        return obj

class UpdateBlogSettingsView(LoginRequiredMixin, UpdateView):
    model = BlogSettings
    template_name = "semantic_admin/blog_settings_edit.html"
    success_url = reverse_lazy('admin:settings:index')
    fields = ('__all__')
    # form_class = UserProfileEditForm

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(UpdateBlogSettingsView, self).get_context_data(**kwargs)
        context['title'] = 'Edit Blog Settings'
        return context

    def get_object(self):
        obj, created = BlogSettings.objects.get_or_create(pk = 1)
        return obj
        
class UpdateArticleFlagView(LoginRequiredMixin, UpdateView):
    model = Flag
    template_name = "semantic_admin/article_flag_edit.html"
    success_url = reverse_lazy('admin:article_types:index')
    form_class = ArticleFlagEditForm

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(UpdateArticleFlagView, self).get_context_data(**kwargs)
        context['article_flags'] = Flag.objects.all()
        context['title'] = context['flag']
        context['button_text'] = "Save"
        return context

class DeleteArticleFlagView(LoginRequiredMixin, DeleteView):
    template_name = "semantic_admin/article_flag_confirm_delete.html"
    model = Flag
    success_url = reverse_lazy('admin:article_types:index')

    def get_context_data(self, **kwargs):
        if 'view' not in kwargs:
            kwargs['view'] = self
        return kwargs

class ContentView(LoginRequiredMixin, FilterView):
    template_name = "semantic_admin/content.html"
    filterset_class = ArticleFilter
    context_object_name = 'article_list'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(ContentView, self).get_context_data(**kwargs)
        context['request'] = self.request
        context['title'] = 'Content Manager'

        # Pagination
        articles = context['filter'].qs
        paginator = Paginator(articles, self.paginate_by)
        page = self.request.GET.get('page')

        try:
            article_list = paginator.page(page)
        except PageNotAnInteger:
            article_list = paginator.page(1)
        except EmptyPage:
            article_list = paginator.page(paginator.num_pages)

        print(paginator.num_pages)

        context['article_list'] = article_list
        return context

class CreateArticleView(LoginRequiredMixin, CreateView):
    template_name = "semantic_admin/edit_article.html"
    success_url = reverse_lazy('admin:content:index')
    form_class = ArticleEditForm

    def get_initial(self):
        initial = super(CreateArticleView, self).get_initial()
        initial["created_date"] = datetime.datetime.now()
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

    def get_success_url(self):
        if 'semantic' in self.request.POST:
            return reverse('admin:semantic:article', kwargs={'slug': self.object.slug})
        else:
            return reverse('admin:content:index')

class UpdateArticleView(LoginRequiredMixin, UpdateView):
    model = Article
    template_name = "semantic_admin/edit_article.html"
    success_url = reverse_lazy('admin:content:index')
    form_class = ArticleEditForm

    def form_valid(self, form):
        form.instance.author = self.request.user

        if self.request.POST:
            if 'publish' in self.request.POST:
                form.instance.publish_article(datetime.datetime.now())
            if 'draft' in self.request.POST:
                form.instance.unpublish_article()

        form.save()
        return super(UpdateArticleView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(UpdateArticleView, self).get_context_data(**kwargs)
        context['title'] = context['article']
        return context

    def get_success_url(self):
        if 'semantic' in self.request.POST:
            return reverse('admin:semantic:article', kwargs={'slug': self.object.slug})
        else:
            return reverse('admin:content:index')

class DeleteArticleView(LoginRequiredMixin, DeleteView):
    template_name = "semantic_admin/article_confirm_delete.html"
    model = Article
    success_url = reverse_lazy('admin:content:index')

    def get_context_data(self, **kwargs):
        if 'view' not in kwargs:
            kwargs['view'] = self
        return kwargs

# class ContentView(LoginRequiredMixin, FilterView):
#     template_name = "semantic_admin/content.html"
#     filterset_class = ArticleFilter
#     context_object_name = 'article_list'
#
#     def get_context_data(self, **kwargs):
#         # Call the base implementation first to get a context
#         context = super(ContentView, self).get_context_data(**kwargs)
#         context['request'] = self.request
#         context['title'] = 'Content Manager'
#         return context

class SemanticView(LoginRequiredMixin, FilterView):
    template_name = "semantic_admin/semantic.html"
    # model = Article
    filterset_class = ArticleFilterSemantic
    context_object_name = 'article_list'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(SemanticView, self).get_context_data(**kwargs)

        # context['last_node_id'] = Semantic.objects.latest('id').id

        if 'slug' in self.kwargs:
            article = Article.objects.get(slug=self.kwargs['slug'])
            context['selected_article'] = article
            context['article_nodes'] = json.dumps(article.semantic_ids())
        else:
            context['article_nodes'] = json.dumps([])

        context['title'] = 'Semantic'
        return context

class DbResetView(LoginRequiredMixin, TemplateView):
    template_name="semantic_admin/reset.html"

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
                if (attribute == "id"):
                    tmp[attribute] = node[attribute]
                if (attribute == "name"):
                    tmp[attribute] = node[attribute]
                    tmp["slug"] = slugify(node[attribute])
            jsonNodesClean.append(tmp)

        for edge in jsonEdges:
            tmp = {}
            tmp["parent_slug"] = slugify(edge["parent_name"])
            tmp["child_slug"] = slugify(edge["child_name"])
            tmp["slug"] = tmp["parent_slug"] + tmp["child_slug"]
            jsonEdgesClean.append(tmp)

        querysetNodes = Semantic.objects.all()
        querysetEdges = SemanticEdge.objects.all()

        serializerNodes = SemanticNodeSerializer(querysetNodes, data=jsonNodesClean, many=True)
        serializerEdges = SemanticEdgeSerializer(querysetEdges, data=jsonEdgesClean, many=True)

        if serializerNodes.is_valid():
            serializerNodes.save()

        if serializerEdges.is_valid():
            serializerEdges.save()

        return HttpResponse(json.dumps({'message': 0}))

    return HttpResponse(json.dumps({'message': 1}))

def add_edge(request):
    if request.method == 'POST':
        jsonData = json.loads(request.body.decode('utf-8'))

        edge = {}

        for attribute in jsonData:
            edge["parent_slug"] = slugify(jsonData["parent_name"])
            edge["child_slug"] = slugify(jsonData["child_name"])
            edge["slug"] = edge["parent_slug"] + edge["child_slug"]

        serializerEdges = SemanticEdgeSerializer(data=edge)

        if serializerEdges.is_valid():
            serializerEdges.save()

            return HttpResponse(json.dumps({'message': 0}))
        else:
            print("ERROR")
            print(serializerEdges.errors)
            return HttpResponse(json.dumps({'message': 1}))


def login(request, template_name):
    login_context = {
        'title': 'Login',
    }
    template_response = views.login(request, template_name, extra_context=login_context)
    return template_response

from django.core.management import call_command
from django.shortcuts import render
from semantic_cms.settings.base import BASE_DIR

@login_required
def reset_database(request):
    path = BASE_DIR + '/reset-output.log'
    call_command('flush', interactive=False)
    with open(path,'w') as f:
        call_command('loaddata', BASE_DIR + '/all.json', stdout=f)

    return render(request, 'semantic_admin/reset_done.html')
