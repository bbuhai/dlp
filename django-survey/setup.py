"""
django-survey
=============

A simple django app that can be used to make simple surveys.
"""

import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
	README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
	name='django-survey',
	version='0.1dev',
	license='BSD',
	author='Bogdan Buhai',
	description='A simple django app for surveys',
	packages=['survey', 'survey.fixtures', 'survey.tests', 'survey.templatetags'],
	include_package_data=True,  # what does this do?	
	classifiers=[
		'Environment :: Web Environment',
		'Framework :: Django',
		'Intended Audience :: Developers'
	]
)
