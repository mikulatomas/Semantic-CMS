from django.db import models
# from django.utils.translation import ugettext_lazy as _

# from taggit_autocomplete.managers import TaggableManager
# from taggit.managers import TaggableManager
from taggit.models import TagBase, GenericTaggedItemBase
#slugify
from django.utils.text import slugify

#time
import datetime
from django.utils import timezone

class Keyword(models.Model):
    """Keyword model for represen keyword in the system, taggit-autocomplete integrated"""

    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50)

    # edited_date will be probably redundant
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
    # TaggedWhatever can also extend TaggedItemBase or a combination of
    # both TaggedItemBase and GenericTaggedItemBase. GenericTaggedItemBase
    # allows using the same tag for different kinds of objects, in this
    # example Food and Drink.

    # Here is where you provide your custom Tag class.
    tag = models.ForeignKey(Keyword, related_name="%(app_label)s_%(class)s_items")
