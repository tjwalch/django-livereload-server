"""django-livereload"""
__version__ = '0.2'
__license__ = 'BSD License'

__author__ = 'Tomas Walch'
__email__ = 'tomaswalch@gmail.com'

__url__ = 'https://github.com/tjwalch/django-livereload-server'


def livereload_port():
    from django.conf import settings
    return int(getattr(settings, 'LIVERELOAD_PORT', 35729))
