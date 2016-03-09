from django import forms
from article.models import Article
from flags.models import Flag
from .models import UserProfile
from datetimewidget.widgets import DateTimeWidget
from django.forms.widgets import TextInput
from django.contrib.auth.models import User
from redactor.widgets import RedactorEditor
from betterforms.multiform import MultiModelForm
from django.contrib.auth.models import User

class ArticleEditForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ["title", "sub_title", "content", "slug", "flag", "created_date", "keywords", "cover_image"]
        # fields = ["title", "sub_title", "content", "slug", "flag", "created_date", "keywords"]
        widgets = {
            'content': RedactorEditor(),
        }

    def __init__(self, *args, **kwargs):
        super(ArticleEditForm, self).__init__(*args, **kwargs)
        self.fields['flag'].empty_label = "Select type of Article"


class ArticleFlagEditForm(forms.ModelForm):
    class Meta:
        model = Flag
        fields = ["name"]
        # fields = ["title", "sub_title", "content", "slug", "flag", "created_date", "keywords"]

class UserEditForm(forms.ModelForm):
    class Meta:
        auto_id="test_%s"
        model = UserProfile
        fields = ["bio", "profile_image"]
        # fields = ('test_string')

class UserInfoEditForm(forms.ModelForm):
    class Meta:
        auto_id="test2_%s"
        model = User
        fields = ["first_name", "last_name", "email"]
        # fields = ('first_name')

class UserProfileEditForm(MultiModelForm):
    form_classes = {
        'info': UserEditForm,
        'user': UserInfoEditForm,
    }
    class Meta:
        auto_id="test_%s"
