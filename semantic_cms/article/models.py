from django.db import models

#https://github.com/dcramer/django-uuidfield
from uuidfield import UUIDField

#Article author
from django.conf import settings
AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')

class Article(models.Model):
    ARTICLE_STATUS = (
        ('D', 'Draft'),
        ('P', 'Published'),
    )

    title = models.CharField(max_length=128)
    sub_title = models.CharField(max_length=128)
    slug = models.SlugField(max_length=50)

    cover_image = models.ImageField(upload_to="images", blank=True, null=True)

    markdown = models.TextField()
    html = models.TextField()

    author = models.ForeignKey(AUTH_USER_MODEL)
    edited_date = models.DateTimeField('date edited')
    created_date = models.DateTimeField('date created')
    published_date = models.DateTimeField('date published')
