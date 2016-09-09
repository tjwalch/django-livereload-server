import os
import itertools
from django.conf import settings
from django.apps import apps
from django.core.management.base import BaseCommand
from ... import livereload_port, server as S, livereload_host


class Command(BaseCommand):
    help = 'Runs a livereload server watching static files and templates.'

    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)
        parser.add_argument(
            'extra',
            nargs='*',
            action='store',
            help='Extra files or directories to watch',
        )
        parser.add_argument(
            '--host', dest='host', default=livereload_host(), help='Host address for livereload sever.'
        )
        parser.add_argument(
            '--port', dest='port', default=livereload_port(), help='Listening port for livereload sever.'
        )

    def handle(self, *args, **options):
        server = S.Server()

        #  The reason not to ask the staticfile finders to list the files is
        # to get a watch when new files are added as well
        for dir in itertools.chain(
                settings.STATICFILES_DIRS,
                getattr(settings, 'TEMPLATE_DIRS', []),
                options.get('extra', []),
                args):
            server.watch(dir)
        for template in getattr(settings, 'TEMPLATES', []):
            for dir in template['DIRS']:
                server.watch(dir)
        for app_config in apps.get_app_configs():
            server.watch(os.path.join(app_config.path, 'static'))
            server.watch(os.path.join(app_config.path, 'templates'))

        server.serve(
            host=options['host'],
            liveport=options['port'],
        )
