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

#import Semantic model
from semantic.models import Semantic

#import Keywords model
from keywords.models import Keyword

#import Flags model
from flags.models import Flag

#slugify
from django.utils.text import slugify


class Article(models.Model):
    """
    Article is basic unit for Semantic CMS, this model holds info about article.
    """

    title = models.CharField(max_length=128)
    sub_title = models.CharField(max_length=128, blank=True, null=True)
    slug = models.SlugField(max_length=50, unique=True, blank=True,  null=True)

    statut = models.CharField(max_length=1,
                                choices=ARTICLE_STATUS,
                                default=DRAFT)

    flag = models.ForeignKey(Flag, null=True, blank=True)

    cover_image = models.ImageField(upload_to="images", blank=True, null=True)

    content = MarkupField(null=True, blank=True)
    html = models.TextField(null=True, blank=True)

    author = models.ForeignKey(User, null=True, blank=True)

    semantic = models.ManyToManyField(Semantic, blank=True)
    keywords = models.ManyToManyField(Keyword, blank=True)

    edited_date = models.DateTimeField('date edited', null=True, blank=True)
    created_date = models.DateTimeField('date created')
    published_date = models.DateTimeField('date published', null=True, blank=True)

    class Meta:
        ordering = ["created_date"]
        get_latest_by = "published_date"

    def __str__(self):
        return self.title

    def generate_html(self):
        self.html = self.content.rendered

    def publish_article(self, time):
        """Change statut of article and dates"""
        self.published_date = time

        self.statut = PUBLISHED

    def edit_article(self, time):
        """Update time of edit article"""
        self.edited_date = time

    def update_slug(self):
        if not self.slug:
            self.slug = slugify(self.title)

    def save(self, *args, **kwargs):
        """Override save"""
        time = timezone.now()

        self.edit_article(time)

        self.update_slug()

        super(Article, self).save(*args, **kwargs) # Call the "real" save() method.
        self.generate_html()
        super(Article, self).save(*args, **kwargs)
