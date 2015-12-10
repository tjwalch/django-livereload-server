========================
django-livereload-server
========================

This django app adds a management command that starts a livereload server watching all your static files and templates as well
as a custom ``runserver`` command that issues livereload requests when the development server is ready after a restart.

Installation
------------

Install package: ::

  $ pip install django-livereload-server

Add ``'livereload'`` to the ``INSTALLED_APPS``, before ``'django.contrib.staticfiles'`` if this is used::

    INSTALLED_APPS = (
        ...
        'livereload',
        ...
    )

Add ``'livereload.middleware.LiveReloadScript'`` to the
``MIDDLEWARE_CLASSES`` (probably at the end)::

    MIDDLEWARE_CLASSES = (
        ...
        'livereload.middleware.LiveReloadScript',
    )

Configuration
-------------
If you need the livereload server to use a different port than the default 35729,
specify it by setting ``LIVERELOAD_PORT`` in ``settings.py``.

Usage
-----
Start the livereload server with: ::

  $ ./manage.py livereload

Extra files and/or paths to watch for changes can be added as positional arguments.

Start the development server as usual with ``./manage.py runserver``. The command now accepts two additional
options:

* ``--nolivereload`` to disable livereload functionality
* ``--livereload-port`` to override both default and settings file specified port

Background
----------
This project is based on a merge of `python-livereload <https://github.com/lepture/python-livereload>`_ and
`django-livereload <https://github.com/Fantomas42/django-livereload>`_, excellent projects both and even better for
smooth django development when combined.
