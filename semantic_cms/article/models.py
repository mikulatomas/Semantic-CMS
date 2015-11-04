#Article models

from django.db import models

#markdown
from markupfield.fields import MarkupField

#time
import datetime
from django.utils import timezone

#Article author
# from django.conf import settings
# AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')
from django.contrib.auth.models import User

#import fields
from .fields import *


class Article(models.Model):
    """
    Article is basic unit for Semantic CMS, this model holds info about article.
    """

    title = models.CharField(max_length=128)
    sub_title = models.CharField(max_length=128)
    slug = models.SlugField(max_length=50)

    statut = models.CharField(max_length=1,
                                choices=ARTICLE_STATUS,
                                default=DRAFT)

    cover_image = models.ImageField(upload_to="images", blank=True, null=True)

    content = MarkupField(null=True, blank=True)
    html = models.TextField(null=True, blank=True)

    author = models.ForeignKey(User, null=True, blank=True)

    edited_date = models.DateTimeField('date edited', null=True, blank=True)
    created_date = models.DateTimeField('date created')
    published_date = models.DateTimeField('date published', null=True, blank=True)

    def publish_article(self, time):

        self.edited_date = time
        self.published_date = time

        self.statut = PUBLISHED

        self.html = self.content.rendered
