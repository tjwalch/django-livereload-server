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

from livereload import livereload_port, livereload_host, livereload_scheme, livereload_injection_host, livereload_injection_port


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

        host = livereload_host()
        if livereload_injection_host() is not None:
            host = livereload_injection_host()

        port = livereload_port()
        if livereload_injection_port() is not None:
            host = livereload_injection_port()

        js_file = 'livereload.js'
        if livereload_scheme() == 'https':
            js_file = 'livereload_wss.js'

         script = soup.new_tag(
            'script', src='%s://%s:%d/%s' % (
                livereload_scheme(),
                host,
                port,
                js_file,
            )
        )
        head.append(script)

        response.content = str(soup)

        return response
