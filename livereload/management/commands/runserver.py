"""Runserver command with livereload"""
import threading
from optparse import make_option
try:
    from urllib.request import urlopen
except ImportError:  # Python 2 fall back
    from urllib2 import urlopen

from django.conf import settings
from django.core.management.color import color_style


if 'django.contrib.staticfiles' in settings.INSTALLED_APPS:
    from django.contrib.staticfiles.management.commands.runserver import \
        Command as RunserverCommand
else:
    from django.core.management.commands.runserver import \
        Command as RunserverCommand

from livereload import livereload_port, livereload_host


class Command(RunserverCommand):
    """
    Command for running the development server with LiveReload.
    """
    option_args = [('--nolivereload',
                    {'action': 'store_false', 'dest': 'use_livereload', 'default': True,
                     'help': 'Tells Django to NOT use LiveReload.'}),
                   ('--livereload-port',
                    {'action': 'store', 'dest': 'livereload_port', 'type': int,
                     'default': livereload_port(),
                     'help': 'Port where LiveReload listens.'}),
                   ('--livereload-host',
                    {'action': 'store', 'dest': 'livereload_host', 'type': str,
                     'default': livereload_host(),
                     'help': 'Address to LiveReload server.'})
                   ]

    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)
        for name, kwargs in self.option_args:
            parser.add_argument(name, **kwargs)

    help = 'Starts a lightweight Web server for development with LiveReload.'

    def message(self, message, verbosity=1, style=None):
        if verbosity:
            if style:
                message = style(message)
            self.stdout.write(message)

    def livereload_request(self, **options):
        """
        Performs the LiveReload request.
        """
        style = color_style()
        verbosity = int(options['verbosity'])
        host = '%s:%d' % (
            options['livereload_host'],
            options['livereload_port'],
        )
        try:
            urlopen('http://%s/forcereload' % host)
            self.message('LiveReload request emitted.\n',
                         verbosity, style.HTTP_INFO)
        except IOError:
            pass

    def get_handler(self, *args, **options):
        """
        Entry point to plug the LiveReload feature.
        """
        handler = super(Command, self).get_handler(*args, **options)
        if options['use_livereload']:
            threading.Timer(1, self.livereload_request, kwargs=options).start()
        return handler
