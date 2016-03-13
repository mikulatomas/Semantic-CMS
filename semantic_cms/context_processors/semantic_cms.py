from semantic_admin.models import BlogSettings

def basic(request):
    blog_settings = BlogSettings.objects.filter(pk = 0)
    context = {}

    if (blog_settings.count() != 0):
        context['blog_settings'] = blog_settings[0]

    return context;
