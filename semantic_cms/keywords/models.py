from django.db import models

class Keyword(models.Model):
    """Keyword model for represen keyword in the system"""

    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)

    edited_date = models.DateTimeField('date edited', null=True, blank=True)
    created_date = models.DateTimeField('date created')

    class Meta:
        ordering = ["name"]
        get_latest_by = "created_date"

    def __str__(self):
        return self.name