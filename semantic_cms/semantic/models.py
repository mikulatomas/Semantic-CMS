#Semantic models

from django.db import models

class Semantic(models.Model):
    """
    Semantic is some kind of category. Every Article can has one or more Semantic category.
    """

    name = models.CharField(max_length=128, unique=True)

    childs = models.ManyToManyField("self", blank=True)

    edited_date = models.DateTimeField('date edited', null=True, blank=True)
    created_date = models.DateTimeField('date created')
