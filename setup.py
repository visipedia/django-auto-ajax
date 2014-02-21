#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


INSTALL_REQUIRES = [
	"django >=1.4",
	"django_jinja",
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
	package_dir = {'django_auto_ajax': 'django_auto_ajax'},
	package_data = {'': ['LICENSE', 'README.md']},
	include_package_data = True,
	install_requires = INSTALL_REQUIRES,

	dependency_links = [
		'git+git://github.com/niwibe/django-jinja.git@b0726105b251bed2b9a8f76e9dde4b4fefeb79ae',
	],
)
