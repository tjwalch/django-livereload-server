import os
from django.conf import settings
from django.apps import apps
from django.core.management.base import BaseCommand
import itertools
from livereload.server import Server
from livereload import livereload_port


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

    def handle(self, *args, **options):
        server = Server()

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
            host='127.0.0.1',
            liveport=livereload_port(),
        )
