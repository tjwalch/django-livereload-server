"""django-livereload"""
__version__ = '0.3.3'
__license__ = 'BSD License'

__author__ = 'Tomas Walch'
__email__ = 'tomaswalch@gmail.com'

__url__ = 'https://github.com/tjwalch/django-livereload-server'


def livereload_port():
    from django.conf import settings
    return int(getattr(settings, 'LIVERELOAD_PORT', 35729))


def livereload_host():
    from django.conf import settings
    return getattr(settings, 'LIVERELOAD_HOST', '127.0.0.1')


def livereload_scheme():
    from django.conf import settings
    return getattr(settings, 'LIVERELOAD_SCHEME', 'http')


def livereload_injection_host():
    from django.conf import settings
    return getattr(settings, 'LIVERELOAD_INJECTION_HOST', None)


def livereload_injection_port():
    from django.conf import settings
    return getattr(settings, 'LIVERELOAD_INJECTION_PORT', None)

