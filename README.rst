-----------------------
django learning program
-----------------------

A small django project built for learning purposes.

Quick start
-----------
1. Create a virtualenv.

2. Clone the project.

3. Install requirements::

    python setup.py install

3. Run::

    python manage.py syncdb --settings=dj_start.settings.prod

4. Load fixtures with::

    python manage.py loaddata survey.json --settings=dj_start.settings.prod

5. Start the server with::

    python manage.py runserver --settings=dj_start.settings.prod

6. Go to `your website http://127.0.0.1:8000/survey/`_ and do the *Survey #1*


Running the tests::

    python manage.py test survey --settings=dj_start.settings.test


