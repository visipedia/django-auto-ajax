import jinja2

from django.template import loader
from django.core.cache import cache
from jinja2.loaders import FileSystemLoader

from django.conf import settings
from django.template.loaders import app_directories

class Loader(FileSystemLoader):

	def __init__(self):
		super(Loader, self).__init__(tuple(settings.TEMPLATE_DIRS) + app_directories.app_template_dirs)

	def get_source(self, environment, template):

		source = cache.get(template)
		# TODO: if template.startswith(template:) ...

		if source is None:
			return super(Loader, self).get_source(environment, template)

		#source, origin = loader.find_template(template)
		return source, template, lambda: False
