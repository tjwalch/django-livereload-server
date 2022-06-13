"""
Middleware for injecting the live-reload script.
"""
import logging
from bs4 import BeautifulSoup

from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
from django.utils.encoding import smart_str


from livereload import livereload_port, livereload_host

logger = logging.getLogger("django.server")

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
            logger.info("No head tag found. Live-reload script not injected.")
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
