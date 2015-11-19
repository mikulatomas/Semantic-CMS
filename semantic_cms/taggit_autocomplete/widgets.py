from django import forms
from django.core.urlresolvers import reverse
from django.conf import settings
from django.utils.safestring import mark_safe

from .utils import edit_string_for_tags


class TagAutocomplete(forms.TextInput):
	input_type = 'text'

	def render(self, name, value, attrs=None):
		list_view = reverse('taggit_autocomplete-list')
		if value is not None and not isinstance(value, str):
			value = edit_string_for_tags([o.tag for o in value.select_related("tag")])
		html = super(TagAutocomplete, self).render(name, value, attrs)

		# js = u'<script type="text/javascript">jQuery().ready(function() { jQuery("#%s").autocomplete("%s", { multiple: true }); });</script>' % (attrs['id'], list_view)
		# js = '<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.2/jquery.min.js"></script><script src="https://ajax.googleapis.com/ajax/libs/jqueryui/1.11.4/jquery-ui.min.js"></script><script type="text/javascript">$(function() {$("#%s").autocomplete({ source: "%s", multiple: true,});});</script>' % (attrs['id'], "http://localhost:8000" + list_view)

		js = '<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.2/jquery.min.js"></script><script src="https://ajax.googleapis.com/ajax/libs/jqueryui/1.10.0/jquery-ui.min.js"></script></script><script type="text/javascript">$(document).ready(function(){$("#%s").tagit({allowSpaces:!0,minLength:2,removeConfirmation:!0,placeholderText:"%s",tagSource:function(e,a){$.ajax({url:"%s",data:{term:e.term},dataType:"json",success:function(e){a($.map(e,function(e){return{label:e,value:e}}))}})}})});</script>' % (attrs['id'], "Write keyword here", list_view)

		tags = '<ul id="keywords"></ul>'

		return mark_safe("\n".join([html, js]))

	# class Media:
	# 	js_base_url = getattr(settings, 'TAGGIT_AUTOCOMPLETE_JS_BASE_URL','%s/jquery-autocomplete' % settings.MEDIA_URL)
	# 	css = {
	# 	    'all': ('%s/jquery.autocomplete.css' % js_base_url,)
	# 	}
	# 	js = (
	# 		'%s/jquery.autocomplete.js' % js_base_url,
	# 		)
