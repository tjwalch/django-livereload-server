"""
Middleware for injecting the live-reload script.
"""
from bs4 import BeautifulSoup

from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
from django.utils.encoding import smart_str

try:
    import html5lib  # noqa
    html5lib_is_installed = True
except ImportError:
    html5lib_is_installed = False


IS_HTML5 = getattr(settings, 'LIVERELOAD_HTML5', html5lib_is_installed)

PARSER = 'html.parser'
if IS_HTML5:
    PARSER = 'html5lib'


class LiveReloadScript(MiddlewareMixin):
    """
    Inject the live-reload script into your webpages.
    """

    def process_response(self, request, response):
        if response.status_code != 200:
            return response

        content_type = response.get(
            'Content-Type', '').split(';')[0].strip().lower()
        if content_type not in ['text/html', 'application/xhtml+xml']:
            return response

        soup = BeautifulSoup(
            smart_str(response.content), PARSER)

        if not getattr(soup, 'head', None):
            return response

        script = soup.new_tag(
            'script', src='http://localhost:35729/livereload.js')
        soup.head.append(script)

        response.content = str(soup)

        return response
