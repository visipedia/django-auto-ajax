from django import shortcuts
from django.core.cache import cache

class SnippetException(Exception):
	pass

def has_snippet(template, snippet):

	if template == snippet['template']:
		return True

	includes = cache.get('template_includes:%s' % template, []) # TODO: None & check
	for i in includes:
		if has_snippet(i, snippet):
			return True

	return False

def render_snippet(request, name, template, data={}):
	snippet_info = cache.get('template_snippets:%s.jinja' % name, None)
	if snippet_info is None:
		raise SnippetException('Snippet info for snippet "%s" not found in cache' % name)

	current = template
	extends = cache.get('template_extends:%s' % template, None)

	new_templates = {}

	found = False
	if has_snippet(current, snippet_info):
		template = snippet_info['template']
		found = True

	while extends is not None and not found:

		# get all blocks from the curret template
		blocks = cache.get('template_blocks:%s' % current, None)
		if blocks is None:
			raise SnippetException('Template blocks for template "%s" not found in cache' % current)

		# find out which template we want to extend in this step
		if has_snippet(extends, snippet_info):
			snippet_template = snippet_info['template']
			found = True
		else:
			snippet_template = extends

		# prepare a new template
		new_name = 'template:%s:%s.jinja' % (current, name)
		new_data = '{%% extends "template:%s:%s.jinja" %%}\n\n' % (snippet_template, name)

		# add all relevant blocks to the new template
		for block in snippet_info['blocks']:
			if block in blocks:
				new_data += '%s' % blocks[block]

		new_templates[new_name] = new_data

		# variables for the next iteration
		current = extends
		extends = cache.get('template_extends:%s' % current, None)

	# here 'current' must already be the snippet's template
	if not found:
		raise SnippetException('Snippet "%s" not found' % name) # TODO: is it the right message?

	# now we can add the new templates to the cache
	for k, v in new_templates.items():
		cache.set(k, v)

	return shortcuts.render(request, 'template:%s:%s.jinja' % (template, name), data)

def render_snippets(request, snippet_names, template, data={}):
	snippets = {}
	for name in snippet_names:
		rendered = render_snippet(request, name, template, data)
		snippets[name] = rendered.content.decode('utf-8')

	return snippets
