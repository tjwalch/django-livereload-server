from django import template
from django.conf import settings
from django.utils.html import format_html
from livereload import livereload_host, livereload_port

register = template.Library()

@register.simple_tag
def livereload_script():
    if settings.DEBUG:
        return format_html(
        """<script src="http://{}:{}/livereload.js"></script>""",
        livereload_host(),
        livereload_port(),
    )
    else:
        return ""
