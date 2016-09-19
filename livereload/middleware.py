"""
Middleware for injecting the live-reload script.
"""
from bs4 import BeautifulSoup

from django.utils.encoding import smart_str
from django.conf import settings
try:
    from django.utils.deprecation import MiddlewareMixin
except ImportError:
    MiddlewareMixin = object

from livereload import livereload_port, livereload_host


class LiveReloadScript(MiddlewareMixin):
    """
    Injects the live-reload script into your webpages.
    """

    def process_response(self, request, response):
        content_type = response.get('Content-Type', '').split(';')[0].strip().lower()
        if (not settings.DEBUG or
                content_type not in ['text/html', 'application/xhtml+xml'] or
                not hasattr(response, 'content')):
            return response

        soup = BeautifulSoup(
            smart_str(response.content),
            'html.parser',
        )

        head = getattr(soup, 'head', None)
        if not head:
            return response

        script = soup.new_tag(
            'script', src='http://%s:%d/livereload.js' % (
                livereload_host(),
                livereload_port(),
            )
        )
        head.append(script)

        response.content = str(soup)

        return response
