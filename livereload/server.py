# -*- coding: utf-8 -*-
"""
    livereload.server
    ~~~~~~~~~~~~~~~~~

    WSGI app server for livereload.

    :copyright: (c) 2013 - 2015 by Hsiaoming Yang
    :license: BSD, see LICENSE for more details.
"""

import os
import shlex
import logging
from subprocess import Popen, PIPE

from tornado.ioloop import IOLoop
from tornado import web
from tornado.log import LogFormatter
from .handlers import LiveReloadHandler, LiveReloadJSHandler
from .handlers import ForceReloadHandler
from .watcher import get_watcher_class
from six import string_types, PY3

import asyncio, sys
if sys.version_info >= (3, 8) and sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

logger = logging.getLogger('livereload')


def shell(cmd, output=None, mode='w', cwd=None, shell=False):
    """Execute a shell command.

    You can add a shell command::

        server.watch(
            'style.less', shell('lessc style.less', output='style.css')
        )

    :param cmd: a shell command, string or list
    :param output: output stdout to the given file
    :param mode: only works with output, mode ``w`` means write,
                 mode ``a`` means append
    :param cwd: set working directory before command is executed.
    :param shell: if true, on Unix the executable argument specifies a
                  replacement shell for the default ``/bin/sh``.
    """
    if not output:
        output = os.devnull
    else:
        folder = os.path.dirname(output)
        if folder and not os.path.isdir(folder):
            os.makedirs(folder)

    if not isinstance(cmd, (list, tuple)) and not shell:
        cmd = shlex.split(cmd)

    def run_shell():
        try:
            p = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE, cwd=cwd,
                      shell=shell)
        except OSError as e:
            logger.error(e)
            if e.errno == os.errno.ENOENT:  # file (command) not found
                logger.error("maybe you haven't installed %s", cmd[0])
            return e
        stdout, stderr = p.communicate()
        if stderr:
            logger.error(stderr)
            return stderr
        #: stdout is bytes, decode for python3
        if PY3:
            stdout = stdout.decode()
        with open(output, mode) as f:
            f.write(stdout)

    return run_shell


class Server(object):
    """Livereload server interface.

    Initialize a server and watch file changes::

        server = Server()
        server.serve()

    :param watcher: A Watcher instance, you don't have to initialize
                    it by yourself. Under Linux, you will want to install
                    pyinotify and use INotifyWatcher() to avoid wasted
                    CPU usage.
    """
    def __init__(self, watcher=None):
        self._setup_logging()
        if not watcher:
            watcher_cls = get_watcher_class()
            watcher = watcher_cls()
        self.watcher = watcher

    def ignore_file_extension(self, extension):
        """
        Configure a file extension to be ignored.

        :param extension: file extension to be ignored
                          (ex. .less, .scss, etc)
        """
        logger.info('Ignoring file extension: {}'.format(extension))
        self.watcher.ignore_file_extension(extension)

    def watch(self, filepath, func=None, delay=None):
        """Add the given filepath for watcher list.

        Once you have intialized a server, watch file changes before
        serve the server::

            server.watch('static/*.stylus', 'make static')
            def alert():
                print('foo')
            server.watch('foo.txt', alert)
            server.serve()

        :param filepath: files to be watched, it can be a filepath,
                         a directory, or a glob pattern
        :param func: the function to be called, it can be a string of
                     shell command, or any callable object without
                     parameters
        :param delay: Delay sending the reload message. Use 'forever' to
                      not send it. This is useful to compile sass files to
                      css, but reload on changed css files then only.
        """
        if isinstance(func, string_types):
            func = shell(func)

        self.watcher.watch(filepath, func, delay)

    def application(self, host, liveport):
        LiveReloadHandler.watcher = self.watcher
        live_handlers = [
            (r'/livereload', LiveReloadHandler),
            (r'/forcereload', ForceReloadHandler),
            (r'/livereload.js', LiveReloadJSHandler)
        ]
        live = web.Application(handlers=live_handlers, debug=False)
        live.listen(liveport, address=host)

    def serve(self, liveport=None, host=None, restart_delay=2):
        """Start serve the server with the given port.

        :param liveport: live reload on this port
        :param host: serve on this hostname, default is 127.0.0.1
        :param open_url_delay: open webbrowser after the delay seconds
        """
        host = host or '127.0.0.1'
        logger.info('Serving on http://%s:%s' % (host, liveport))

        self.application(host, liveport=liveport)

        try:
            self.watcher._changes.append(('__livereload__', restart_delay))
            LiveReloadHandler.start_tasks()
            IOLoop.instance().start()
        except KeyboardInterrupt:
            logger.info('Shutting down...')

    def _setup_logging(self):
        logger.setLevel(logging.INFO)

        channel = logging.StreamHandler()
        channel.setFormatter(LogFormatter())
        logger.addHandler(channel)

        # need a tornado logging handler to prevent IOLoop._setup_logging
        logging.getLogger('tornado').addHandler(channel)
