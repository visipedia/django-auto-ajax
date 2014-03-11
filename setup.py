from setuptools import setup, find_packages


INSTALL_REQUIRES = [
	"django >=1.4",
	"django_jinja==b0726105b251bed2b9a8f76e9dde4b4fefeb79ae",
]

setup(
	name = "django-auto-ajax",
	version = "dev",
	description = "The automatic ajax solution for Django with Jinja2.",
	long_description = "",
	keywords = "django, visipedia, jinja, jinja2, ajax",
	author = "Jan Jakes, Tomas Matera",
	author_email = "jan@jakes.pro",
	url = "https://github.com/visipedia/django-auto-ajax",
	license = "MIT",
	packages = find_packages(),
	include_package_data = True,
	install_requires = INSTALL_REQUIRES,

	dependency_links = [
		'git+git://github.com/niwibe/django-jinja.git@b0726105b251bed2b9a8f76e9dde4b4fefeb79ae#egg=django-jinja-b0726105b251bed2b9a8f76e9dde4b4fefeb79ae',
	],
)
