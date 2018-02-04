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

Add ``'livereload.middleware.LiveReloadScript'`` to
``MIDDLEWARE_CLASSES`` (probably at the end)::

    MIDDLEWARE_CLASSES = (
        ...
        'livereload.middleware.LiveReloadScript',
    )

Or to ``MIDDLEWARE`` for Django >= 1.10::

    MIDDLEWARE = [
        ...
        'livereload.middleware.LiveReloadScript',
    ]

This will inject the ``livereload.js`` script into your webpages if ``DEBUG`` setting is on.

Configuration
-------------
If you need the livereload server to use a different host and port than the default 127.0.0.1 and 35729,
specify them by setting ``LIVERELOAD_HOST`` and ``LIVERELOAD_PORT`` in ``settings.py``.

Usage
-----
Start the livereload server. (**NOTE**: This is not a replacement for ``runserver``. See below for more details.) ::

  $ ./manage.py livereload

Extra files and/or paths to watch for changes can be added as positional arguments. By default livereload server watches the files that are found by your staticfiles finders and your template loaders. ::

  $ ./manage.py livereload path/to/my-extra-directory/

Host and port can be overridden with ``--host`` and ``port`` options. ::

  $ ./manage.py livereload --host=myhost.com --port=9090

Start the development server as usual with ``./manage.py runserver``. The command now accepts three additional
options:

* ``--nolivereload`` to disable livereload functionality
* ``--livereload-host`` to override both default and settings file specified host address
* ``--livereload-port`` to override both default and settings file specified port

Background
----------
This project is based on a merge of `python-livereload <https://github.com/lepture/python-livereload>`_ and
`django-livereload <https://github.com/Fantomas42/django-livereload>`_, excellent projects both and even better for
smooth django development when combined.
