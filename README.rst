-----------------------
django learning program
-----------------------

A small django project built for learning purposes.

Quick start
-----------
1. Create a virtualenv.
2. Install the project::

    pip install <path_to_dj_start_tag.gz>

3. Run::

    python manage.py syncdb --settings=dj_start.settings.prod

4. Load fixtures with::

    python manage.py loaddata survey.json

5. Start the server with::

    python manage.py runserver --settings=dj_start.settings.prod

6. Enjoy