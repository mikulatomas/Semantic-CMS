#Article models
from django.db import models

#markdown
from markupfield.fields import MarkupField

#time
import datetime
from django.utils import timezone

#Article author
from django.contrib.auth.models import User

#import fields
from .fields import *

#import Semantic model
from semantic.models import Semantic

#import Keywords model
from keywords.models import Keyword
from keywords.models import TaggedArticle
from keywords.managers import TaggableManager

#import Flags model
from flags.models import Flag

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
    slug = models.SlugField(max_length=50, unique=True)

    status = models.CharField(max_length=1,
                                choices=ARTICLE_STATUS,
                                default=DRAFT)

    flag = models.ForeignKey(Flag, null=True, blank=True)

    cover_image = ProcessedImageField(upload_to=upload_to_id_image,
                                           processors=[ResizeToFill(3000, 1000)],
                                           format='JPEG',
                                           options={'quality': default_quality}, blank=True, null=True)

    content = RedactorField(verbose_name='Content')

    author = models.ForeignKey(User, null=True, blank=True)

    semantic = models.ManyToManyField(Semantic, blank=True)
    keywords = TaggableManager(blank=True, through=TaggedArticle)

    created_date = models.DateTimeField('date created')
    updated_date = models.DateTimeField(auto_now=True)
    published_date = models.DateTimeField('date published', null=True, blank=True)

    class Meta:
        ordering = ["created_date"]
        get_latest_by = "published_date"

    def __str__(self):
        return self.title

    def is_draft(self):
        return self.status == DRAFT

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

    def semantic_ids(self):
        result = []
        for semantic in self.semantic.all():
            result.append(semantic.id)
        return result


    def reset_semantic_ids(self, ids):
        self.semantic.clear()
        for id in ids:
            self.semantic.add(Semantic.objects.get(pk = id))

    def number_of_semantic(self):
        return self.semantic.count()

    def semantic_similar_with(self, source, target):
        """Return similariti of semantic category for 2 articles, for example 0,5 = 50% similarity"""

        source_number_of_semantic = source.semantic.count()
        target_number_of_semantic = target.semantic.count()
        number_of_same = 0

        for semantic in source.semantic.all():
            if semantic in target.semantic.all():
                number_of_same = number_of_same + 1

        for semantic in source.semantic.all():
            for semantic_parent in semantic.parents():
                if semantic_parent in target.semantic.all():
                    number_of_same = number_of_same + 1

                for semantic_target in target.semantic.all():
                    if semantic_parent in semantic_target.parents():
                        number_of_same = number_of_same + 1

        if (number_of_same == 0):
            return 0;
        else:
            return number_of_same / source_number_of_semantic

    def return_similar_articles(self, number):
        """Return number of similar article to this one"""

        all_articles = Article.objects.filter(status='P')
        all_articles = all_articles.exclude(pk=self.pk)

        newlist = sorted(all_articles, key=lambda x: x.semantic_similar_with(self, x), reverse=True)

        return newlist[:number]
