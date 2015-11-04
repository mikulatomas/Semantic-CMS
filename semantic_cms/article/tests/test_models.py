import datetime

from django.utils import timezone
from django.test import TestCase

from article.models import Article
from article.fields import *

class ArticleTestCase(TestCase):
    """ArticleTestCase"""

    def setUp(arg):
        time = timezone.now()

        title = "Test article"
        sub_title = "Sub title of test article"
        slug = "test_article"

        content="*Test* Markdown"

        article = Article(title=title, sub_title=sub_title, slug=slug, content=content, content_markup_type='markdown', created_date=time)

        article.save()

    def test_article_markdown(self):
        """Test if markdown works well"""

        article = Article.objects.get(title="Test article")

        self.assertEqual(article.content.rendered, "<p><em>Test</em> Markdown</p>")

    def test_article_publish(self):
        """Test of publish_article function"""

        time = timezone.now()

        article = Article.objects.get(title="Test article")

        article.publish_article(time)

        self.assertEqual(article.edited_date, time)
        self.assertEqual(article.published_date, time)
        self.assertEqual(article.statut, PUBLISHED)
        self.assertEqual(article.html, "<p><em>Test</em> Markdown</p>")
