# -*- coding: utf-8 -*-
import os
import os.path

import cherrypy
from cherrypy.process import plugins
from django.core.wsgi import get_wsgi_application

from mgp import settings

__all__ = ['DjangoAppPlugin']


class DjangoAppPlugin(plugins.SimplePlugin):
    def __init__(self, bus, settings_module):
        """ CherryPy engine plugin to configure and mount
        the Django application onto the CherryPy server.
        """
        plugins.SimplePlugin.__init__(self, bus)
        self.settings_module = settings_module

    def start(self):
        """ When the bus starts, the plugin is also started
        and we load the Django application. We then mount it on
        the CherryPy engine for serving as a WSGI application.
        We let CherryPy serve the application's static files.
        """
        cherrypy.log("Loading and serving the Django application")
        cherrypy.tree.graft(get_wsgi_application())
        settings_module = self.settings_module

        # App specific static handler
        static_handler = cherrypy.tools.staticdir.handler(
            section="/",
            dir=os.path.split(settings_module.STATIC_ROOT)[1],
            root=os.path.abspath(os.path.split(settings_module.STATIC_ROOT)[0])
        )
        cherrypy.tree.mount(static_handler, settings_module.STATIC_URL)


if __name__ == '__main__':
    cherrypy.config.update({
        'global': {
            'server.socket_host': "0.0.0.0",
            'server.socket_port': 8000,
            'log.screen': True,
            'engine.autoreload.on': True,
            'engine.SIGHUP': None,
            'engine.SIGTERM': None
        }
    })

    os.environ['DJANGO_SETTINGS_MODULE'] = 'mgp.settings_aws'
    DjangoAppPlugin(cherrypy.engine, settings).subscribe()

    cherrypy.engine.start()
    cherrypy.engine.block()
