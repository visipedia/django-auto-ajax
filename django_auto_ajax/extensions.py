import os
import re
from django.core.cache import cache
from jinja2 import nodes
from jinja2.ext import Extension

class SnippetsExtension(Extension):

	tags = set(['snippet'])

	def preprocess(self, source, name, filename=None):

		if name.startswith('template_snippets:'):
			return source

		if name.startswith('template:'):
			return source

		#cached = cache.get('template_cached_list', {})
		#changed = os.path.getmtime(filename)

		#if name not in cached or cached[name]['changed'] < changed:
		#	cached[name] = {'filename': filename, 'changed': changed}
		#	cache.set('template_cached_list', cached)
		if True: # TODO: solve cache (or do this always? or split it away?)

			snippets = self._find_snippets(name, source)

			for k, v in snippets.items():
				if k == '%%page%%': continue

				value = {
					'template': name,
					'blocks': self._find_blocks(v).keys()
				}
				cache.set('template_snippets:%s.jinja' % k, value)
				cache.set('template:%s:%s.jinja' % (name, k), v)

			# save all the blocks from this template
			cache.set('template_blocks:%s' % name, self._find_blocks(source))

			# save wheter the template extends another
			matched = re.search(r'{%\s*extends\s+["\'](?P<name>[^%]+)["\']\s*%}', source)
			if matched is not None:
				cache.set('template_extends:%s' % name, matched.group('name'))

			# save which templates are included
			includes = []
			for matched in re.finditer(r'{%\s*include\s+["\'](?P<name>[^%]+)["\']\s*%}', source):
				includes.append(matched.group('name'))
			cache.set('template_includes:%s' % name, includes)

		return source

	def _find_blocks(self, source):
		splitted = re.split(r'({%\s*(?:(?:block\s+[^%]+)|endblock)\s*%})', source)

		names = []
		blocks = {}

		for part in splitted:
			matched = re.match(r'{%\s*block\s["\']?(?P<name>[^%]+)["\']?\s*%}', part)

			if matched is not None:
				n = matched.group('name')
				names.append(n)
				blocks[n] = part
			else:
				for n in names:
					blocks[n] += part

				if re.match(r'{%\s*endblock\s*%}', part) is not None:
					names.pop()

		return blocks

	def _find_snippets(self, name, source):
		splitted = re.split(r'({%\s*(?:(?:snippet\s+[^%]+)|endsnippet)\s*%})', source)

		names = ['%%page%%']
		snippets = {'%%page%%' : ''}

		for part in splitted:
			matched = re.match(r'{%\ssnippet\s["\'](?P<name>[^%]+)["\']\s%}', part)
			if matched is not None:
				n = matched.group('name')
				snippets[names[-1]] += '\n<div id="snippet--%s">\n\t{%% include "template:%s:%s.jinja" %%}\n</div>\n' % (n, name, n)

				names.append(n)
				snippets[n] = ''

			elif re.match(r'{%\sendsnippet\s%}', part) is not None:
				names.pop()
			else:
				snippets[names[-1]] += part

		return snippets

	def parse(self, parser):

		lineno = next(parser.stream).lineno
		args = [parser.parse_expression()]
		body = parser.parse_statements(['name:endsnippet'], drop_needle=True)
		return nodes.CallBlock(self.call_method('_snippet_support', args), [], [], body).set_lineno(lineno)

	def _snippet_support(self, name, caller):
		return '<div id="snippet--%s">%s</div>' % (name, caller())
