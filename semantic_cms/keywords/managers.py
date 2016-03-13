from django.contrib.admin.widgets import AdminTextInputWidget
# from django.utils.translation import ugettext_lazy as _

from taggit.forms import TagField
from taggit.managers import TaggableManager as BaseTaggableManager

from .widgets import TagAutocomplete

class TaggableManager(BaseTaggableManager):
    """Updated TaggableManager from django-taggit for enable autocomplete"""

    def formfield(self, form_class=TagField, **kwargs):
        defaults = {
            "label": self.verbose_name,
            "help_text": self.help_text,
            "required": not self.blank
        }

        # Adding special widget to default input
        defaults['widget'] = TagAutocomplete

        defaults.update(kwargs)

        return form_class(**defaults)
