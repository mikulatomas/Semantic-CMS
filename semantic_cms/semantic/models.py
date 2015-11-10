#Semantic models

from django.db import models

class Semantic(models.Model):
    """
    Semantic is some kind of category. Every Article can has one or more Semantic category.
    """

    name = models.CharField(max_length=128, unique=True)

    relationships = models.ManyToManyField("self", through="Relationship",blank=True, symmetrical=False, related_name="related_to")

    edited_date = models.DateTimeField('date edited', null=True, blank=True)
    created_date = models.DateTimeField('date created')

    def __str__(self):
        return self.name

class Relationship(models.Model):
    parent = models.ForeignKey(Semantic, related_name="parents")
    child = models.ForeignKey(Semantic, related_name="childs")

    def __str__(self):
        return self.parent.name + " -> " + self.child.name
