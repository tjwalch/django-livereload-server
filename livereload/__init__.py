"""django-livereload"""
__version__ = '0.4'
__license__ = 'BSD License'

__author__ = 'Tomas Walch'
__email__ = 'tomaswalch@gmail.com'

__url__ = 'https://github.com/tjwalch/django-livereload-server'


def livereload_port():
    from django.conf import settings
    return int(getattr(settings, 'LIVERELOAD_PORT', None) or 35729)


def livereload_host():
    from django.conf import settings
    return getattr(settings, 'LIVERELOAD_HOST', None) or '127.0.0.1'
