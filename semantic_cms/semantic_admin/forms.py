from django import forms
from article.models import Article
from datetimewidget.widgets import DateTimeWidget
from django.forms.widgets import TextInput


class ArticleEditForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ["title", "sub_title", "content", "slug", "flag", "created_date", "keywords", "author"]
        widgets = {
            # 'author': TextInput(attrs={'cols': 80, 'rows': 20}),
            'author': TextInput(attrs={'readonly':'readonly'}),
        }

    def __init__(self, *args, **kwargs):
        super(ArticleEditForm, self).__init__(*args, **kwargs)
        self.fields['flag'].empty_label = "Select type of Article"
