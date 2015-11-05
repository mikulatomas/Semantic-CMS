from django.db import models

#time
import datetime
from django.utils import timezone

class Keyword(models.Model):
    """Keyword model for represen keyword in the system"""

    name = models.CharField(blank=True, max_length=50)
    slug = models.SlugField(max_length=50)

    edited_date = models.DateTimeField('date edited', null=True, blank=True)
    created_date = models.DateTimeField('date created')

    class Meta:
        ordering = ["name"]
        get_latest_by = "created_date"
