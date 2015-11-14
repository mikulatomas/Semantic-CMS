from django import forms
from article.models import Article
from datetimewidget.widgets import DateTimeWidget

class ArticleEditForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ["title", "sub_title", "content", "slug", "flag", "created_date"]

        widgets = {
            'title': forms.TextInput(),
            'sub_title': forms.TextInput(),
            'content': forms.Textarea(),
            'slug': forms.TextInput(),
            'flag': forms.Select(),
            'created_date': forms.DateTimeInput(),
        }

    def __init__(self, *args, **kwargs):
        super(ArticleEditForm, self).__init__(*args, **kwargs)
        self.fields['flag'].empty_label = "Select type of Article"
