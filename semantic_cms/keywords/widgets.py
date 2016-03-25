from django import forms
from django.core.urlresolvers import reverse
from django.conf import settings
from django.utils.safestring import mark_safe

from .utils import edit_string_for_tags


class TagAutocomplete(forms.TextInput):
	input_type = 'text'

	def render(self, name, value, attrs=None):
		list_view = reverse('keywords-list')
		if value is not None and not isinstance(value, str):
			value = edit_string_for_tags([o.tag for o in value.select_related("tag")])
		html = super(TagAutocomplete, self).render(name, value, attrs)

		js = '<script type="text/javascript">$(document).ready(function(){$("#%s").tagit({allowSpaces:!0,minLength:2,removeConfirmation:!0,placeholderText:"%s",preprocessTag:function(val){return val.substring(0,15);},tagSource:function(e,a){$.ajax({url:"%s",data:{term:e.term},dataType:"json",success:function(e){a($.map(e,function(e){return{label:e,value:e}}))}})}})});</script>' % (attrs['id'], "Write keyword here", list_view)

		return mark_safe("\n".join([html, js]))

	class Media:
		js = ('https://ajax.googleapis.com/ajax/libs/jquery/1.11.2/jquery.min.js', 'https://ajax.googleapis.com/ajax/libs/jqueryui/1.10.0/jquery-ui.min.js')
