=============
django-survey
=============

A simple django app what can be used for simple surveys/questionaires.

Quick start
-----------

1. Add 'survey' to your INSTALLED_APPS setting like this::

	INSTALLED_APPS = (
		...
		'survey',
	)

2. Include the survey URLconf in your project urls.py like this::

	url(r'^survey/', include('survey.urls', namespace='survey')),

3. Run `python manage.py syncdb`

4. (Optional) Load fixtures with `python mange.py loaddata survey.json`

