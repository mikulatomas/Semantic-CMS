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
from keywords.models import TaggedArticle
from keywords.managers import TaggableManager
# from taggit.managers import TaggableManager
# from taggit.models import TaggedItemBase

#import Flags model
from flags.models import Flag

# #slugify
# from django.utils.text import slugify

#redactor
from redactor.fields import RedactorField

#Images
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from semantic_cms.image_tools import upload_to_id_image, default_quality

class Article(models.Model):
    """
    Article is basic unit for Semantic CMS, this model holds info about article.
    """

    title = models.CharField(max_length=128)
    sub_title = models.CharField(max_length=128, blank=True, null=True)
    slug = models.SlugField(max_length=50, unique=True, blank=True,  null=True)

    status = models.CharField(max_length=1,
                                choices=ARTICLE_STATUS,
                                default=DRAFT)

    flag = models.ForeignKey(Flag, null=True, blank=True)

    # cover_image = models.ImageField(upload_to="articles/", blank=True, null=True)
    cover_image = ProcessedImageField(upload_to=upload_to_id_image,
                                           processors=[ResizeToFill(3000, 1000)],
                                           format='JPEG',
                                           options={'quality': default_quality}, blank=True, null=True)

    content = RedactorField(verbose_name='Content')
    # content = MarkupField(default_markup_type='markdown', null=True, blank=True)
    # html = models.TextField(null=True, blank=True)

    author = models.ForeignKey(User, null=True, blank=True)

    semantic = models.ManyToManyField(Semantic, blank=True)
    # keywords = models.ManyToManyField(Keyword, blank=True)
    keywords = TaggableManager(blank=True, through=TaggedArticle)


    # edited_date = models.DateTimeField('date edited', null=True, blank=True)
    created_date = models.DateTimeField('date created')
    # created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    published_date = models.DateTimeField('date published', null=True, blank=True)

    class Meta:
        ordering = ["created_date"]
        get_latest_by = "published_date"

    def __str__(self):
        return self.title

    def is_draft(self):
        return self.status == DRAFT

    # def generate_html(self):
    #     self.html = self.content.rendered

    def publish_article(self, time):
        """Change status of article and dates"""
        self.published_date = time

        self.status = PUBLISHED

    def unpublish_article(self):
        """Change status of article """
        self.published_date = None;
        self.status = DRAFT

    def edit_article(self, time):
        """Update time of edit article"""
        self.edited_date = time

    # def update_slug(self):
    #     if not self.slug:
    #         self.slug = slugify(self.title)

    def semantic_ids(self):
        result = []
        for semantic in self.semantic.all():
            result.append(semantic.id)
        return result


    def reset_semantic_ids(self, ids):
        self.semantic.clear()
        for id in ids:
            self.semantic.add(Semantic.objects.get(pk = id))

    # Do I need this???
    # def type(self):
    #     return "article";

    def save(self, *args, **kwargs):
        """Override save"""
        time = timezone.now()

        self.edit_article(time)

        # self.update_slug()

        super(Article, self).save(*args, **kwargs) # Call the "real" save() method.
        # self.generate_html()
        # super(Article, self).save(*args, **kwargs)
