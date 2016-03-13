from django.db import models
from taggit.models import TagBase, GenericTaggedItemBase
#slugify
from django.utils.text import slugify

class Keyword(models.Model):
    """Keyword model for represen keyword in the system, taggit-autocomplete integrated"""

    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        get_latest_by = "created_date"
        verbose_name = "Keyword"
        verbose_name_plural = "Keywords"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Keyword, self).save(*args, **kwargs)

class TaggedArticle(GenericTaggedItemBase):
    tag = models.ForeignKey(Keyword, related_name="%(app_label)s_%(class)s_items")
