"""
Middleware for injecting the live-reload script.
"""
from bs4 import BeautifulSoup

from django.utils.encoding import smart_str
from django.conf import settings
from livereload import livereload_port


class LiveReloadScript(object):
    """
    Inject the live-reload script into your webpages.
    """

    def process_response(self, request, response):
        content_type = response.get('Content-Type', '').split(';')[0].strip().lower()
        if content_type not in ['text/html', 'application/xhtml+xml'] or settings.DEBUG == False:
            return response

        soup = BeautifulSoup(
            smart_str(response.content),
            'html.parser',
        )

        if not getattr(soup, 'head', None):
            return response

        script = soup.new_tag(
            'script', src='http://localhost:%d/livereload.js' % livereload_port(),
        )
        soup.head.append(script)

        response.content = str(soup)

        return response
