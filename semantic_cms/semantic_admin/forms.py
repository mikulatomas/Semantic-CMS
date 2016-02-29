from django import forms
from article.models import Article
from datetimewidget.widgets import DateTimeWidget
from django.forms.widgets import TextInput
from django.contrib.auth.models import User
from redactor.widgets import RedactorEditor

class ArticleEditForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ["title", "sub_title", "content", "slug", "flag", "created_date", "keywords", "author", "cover_image"]
        # fields = ["title", "sub_title", "content", "slug", "flag", "created_date", "keywords"]
        widgets = {
            'author': TextInput(attrs={'readonly':'readonly'}),
            'content': RedactorEditor(),
        }

    def __init__(self, *args, **kwargs):
        super(ArticleEditForm, self).__init__(*args, **kwargs)
        self.fields['flag'].empty_label = "Select type of Article"
