from django.db import models

#slugify
from django.utils.text import slugify

class Flag(models.Model):
    """Flag model, you can set up flag for your content"""

    name = models.CharField(max_length=25, unique=True)
    slug = models.SlugField(max_length=50, unique=True)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        get_latest_by = "created_date"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """Override save"""
        self.slug = slugify(self.name)

        super(Flag, self).save(*args, **kwargs)
