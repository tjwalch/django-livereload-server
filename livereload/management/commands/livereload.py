import os
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
            '--ignore-file-extensions',
            action='store',
            help='File extensions to ignore',
        )
        parser.add_argument(
            '--host', dest='host', default=livereload_host(), help='Host address for livereload sever.'
        )
        parser.add_argument(
            '--port', dest='port', default=livereload_port(), help='Listening port for livereload sever.'
        )
        parser.add_argument(
            '--ignore-template-dirs',
            dest='ignore-template-dirs',
            action='store_true',
            help="Prevent watching template directories",
        )
        parser.add_argument(
            '--ignore-static-dirs',
            dest='ignore-static-dirs',
            action='store_true',
            help="Prevent watching staticfiles directories",
        )
        parser.add_argument(
            '-w', '--wait', dest='delay', type=float, default=0, help='Delay before reloading page in seconds'
        )

    def handle(self, *args, **options):
        server = S.Server()
        watch_dirs = options.get('extra', [])
        app_configs = apps.get_app_configs()

        if options['ignore-template-dirs'] is not True:
            watch_dirs.extend(getattr(settings, 'TEMPLATE_DIRS', []))
            for template in getattr(settings, 'TEMPLATES', []):
                if 'DIRS' in template:
                    watch_dirs.extend(template['DIRS'])
            watch_dirs.extend([os.path.join(app_config.path, 'templates')
                               for app_config in app_configs])

        if options['ignore-static-dirs'] is not True:
            watch_dirs.extend(getattr(settings, 'STATICFILES_DIRS', []))
            watch_dirs.extend([os.path.join(app_config.path, 'static')
                               for app_config in app_configs])

        if options['ignore_file_extensions']:
            ignore_file_extensions = options.get('ignore_file_extensions', '').split(',')
            for extension in ignore_file_extensions:
                if not extension.startswith('.'):
                    extension = f'.{extension}'
                server.ignore_file_extension(extension.strip())

        for dir in filter(None, watch_dirs):
            server.watch(str(dir), delay=options['delay'])  # Watcher can only handle strings, not Path objects

        server.serve(
            host=options['host'],
            port=options['port'],
        )
