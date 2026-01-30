============
django-polls
============

django-polls is a Django app to conduct web-based polls. For each
question, visitors can choose between a fixed number of answers.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "polls" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...,
        "django_polls",
    ]

2. Include the polls URLconf in your project urls.py like this::

    path("polls/", include("django_polls.urls")),

3. Run ``python manage.py migrate`` to create the models.

4. Start the development server and visit the admin to create a poll.

5. Visit the ``/polls/`` URL to participate in the poll.

JSON API
--------

This app also exposes a lightweight JSON API under the ``/polls/api/``
prefix. The API mirrors the HTML views and is useful for single-page apps
or integrations.

- GET /polls/api/ - list published polls (id, question_text, pub_date)
- GET /polls/api/<id>/ - poll detail with choices
- POST /polls/api/<id>/vote/ - submit a vote using JSON body: ``{"choice_id": <id>}``
- GET /polls/api/<id>/results/ - poll results (choice_text and votes)

Notes
-----

- The API only exposes polls whose ``pub_date`` is in the past (no future
  polls are returned).
- The project uses the standard Django testing framework. Run the app
  tests with::

    python manage.py test

- Add a virtual environment, install Django, and run migrations before
  starting the server.
