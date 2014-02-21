import json
import os
from django import shortcuts
from django.http import HttpResponse
from django.contrib import messages
from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.template.base import TemplateDoesNotExist
from django_jinja.base import env

from .snippets import render_snippets, SnippetException

def response(request, template, data={}):

	if request.is_ajax():
		snippets = {}
		if 'invalidated_snippets' in request.session:
			snippet_names = request.session['invalidated_snippets']
			if len(messages.get_messages(request)) > 0:
				snippet_names.append('alerts')

			# now simply try to render the snippets, if there are not cached yet,
			# we'll try to render the whole template to get them into the cache
			try:
				snippets = render_snippets(request, snippet_names, template, data)
			except (SnippetException, TemplateDoesNotExist):

				# remove the temlate from Jinja2 cache to force it's reload
				#if template in env.cache:
				#	del env.cache[template]
				env.cache.clear()
				# removing only the template (as above) is not enough!
				# because it can extend/include some other templates
				# and we need them to re-render too!

				shortcuts.render(request, template, data)
				snippets = render_snippets(request, snippet_names, template, data)

			del request.session['invalidated_snippets']

		response = {
			'url': request.path,
			'snippets': snippets
		}
		return HttpResponse(json.dumps(response), mimetype='application/json')

	else:
		if 'invalidated_snippets' in request.session:
			del request.session['invalidated_snippets']
		return shortcuts.render(request, template, data)

def ajax_response(data={}):
	 return HttpResponse(json.dumps(data), mimetype='application/json')

def redirect(request, to, permanent=False, *args, **kwargs):
	if request.is_ajax():
		response = {
			'redirect': reverse(to)
		}
		return HttpResponse(json.dumps(response), mimetype='application/json')
	else:
		return shortcuts.redirect(to, permanent=permanent, *args, **kwargs)

def invalidate(request, snippets=[]):
	if not isinstance(snippets, list): snippets = [snippets]
	if 'invalidated_snippets' not in request.session:
		request.session['invalidated_snippets'] = []
	request.session['invalidated_snippets'] += snippets
