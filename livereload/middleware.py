"""
Middleware for injecting the live-reload script.
"""
from django.conf import settings
from django.utils.encoding import smart_str
from django.utils.html import format_html

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
        content_type = response.get("Content-Type", "").split(";")[0].strip().lower()
        if (
            not settings.DEBUG
            or content_type not in ["text/html", "application/xhtml+xml"]
            or not hasattr(response, "content")
        ):
            return response

        content = smart_str(response.content)
        insertion_point = "</head>"
        livereload_script_tag = format_html(
            """<script src="http://{}:{}/livereload.js"></script>""",
            livereload_host(),
            livereload_port(),
        )
        # only insert the livereload_script_tag once
        insertion_count = 1
        response.content = content.replace(
            insertion_point,
            livereload_script_tag + insertion_point,
            insertion_count,
        )

        return response
