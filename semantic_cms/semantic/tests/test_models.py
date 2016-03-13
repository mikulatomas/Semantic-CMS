import datetime

from django.utils import timezone
from django.test import TestCase

from semantic.models import Semantic

class SemanticTestCase(TestCase):
    """SemanticTestCase"""

    def setUp(self):
        """
        Setup everything for testing
        """
        time = timezone.now()

        comuters = Semantic.objects.create(name="Computers", edited_date=time, created_date=time)
        software = Semantic.objects.create(name="Software", edited_date=time, created_date=time)
        hardware = Semantic.objects.create(name="Hardware", edited_date=time, created_date=time)
        games = Semantic.objects.create(name="Games", edited_date=time, created_date=time)

        art = Semantic.objects.create(name="Art", edited_date=time, created_date=time)
        graphics = Semantic.objects.create(name="Graphic Design", edited_date=time, created_date=time)

        computers.childs.add(software)
        computers.childs.add(hardware)
        computers.save()

        software.childs.add(games)
        software.save()

        art.childs.add(graphics)
        art.save()

        graphics.childs(games)
        graphics.save()
