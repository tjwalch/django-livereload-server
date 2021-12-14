"""Runserver command with livereload"""
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


class Command(RunserverCommand):
    """
    Command for running the development server with LiveReload.
    """
    # Allow a settings option to set the default port
    livereload_default_port = getattr(settings, 'LIVERELOAD_PORT', '35729')
    # Allow a settings option to set the default host
    livereload_default_host = getattr(settings, 'LIVERELOAD_HOST', 'localhost')

    if callable(getattr(RunserverCommand, 'add_arguments', None)):
        def add_arguments(self, parser):
            super(Command, self).add_arguments(parser)
            parser.add_argument('--nolivereload', action='store_false',
                                dest='use_livereload', default=True,
                                help='Tells Django to NOT use LiveReload.')
            parser.add_argument('--livereload-port', action='store',
                                dest='livereload_port',
                                default=self.livereload_default_port,
                                help='Port where LiveReload listen.')
            parser.add_argument('--livereload-host', action='store',
                                dest='livereload_host',
                                default=self.livereload_default_host,
                                help='Host where LiveReload is running.')

    else:
        option_list = RunserverCommand.option_list + (
            make_option('--nolivereload', action='store_false',
                        dest='use_livereload', default=True,
                        help='Tells Django to NOT use LiveReload.'),
            make_option('--livereload-port', action='store',
                        dest='livereload_port',
                        default=livereload_default_port,
                        help='Port where LiveReload listen.'),
            make_option('--livereload-host', action='store',
                        dest='livereload_host',
                        default=livereload_default_host,
                        help='Host where LiveReload is running.'),
        )

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
        host = '%s:%s' % (options['livereload_host'],
                          options['livereload_port'])
        try:
            urlopen('http://%s/changed?files=.' % host)
            self.message('LiveReload request emitted.\n',
                         verbosity, style.HTTP_INFO)
        except IOError as e:
            self.stdout.write(
                self.style.WARNING('LiveReload exception: %s' % e)
            )
            pass

    def get_handler(self, *args, **options):
        """
        Entry point to plug the LiveReload feature.
        """
        handler = super(Command, self).get_handler(*args, **options)
        if options['use_livereload']:
            self.livereload_request(**options)
        return handler
