# -*- coding: utf-8 -*-
import os
import os.path

import cherrypy
from cherrypy.process import plugins
from django.core.wsgi import get_wsgi_application
import win32serviceutil
import win32service


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


class MyService(win32serviceutil.ServiceFramework):
    """NT Service."""
    
    _svc_name_ = "MGP_SERVICE"
    _svc_display_name_ = "MGP Service"

    def SvcDoRun(self):
        cherrypy.config.update({
            'global': {
                'server.socket_host': "0.0.0.0",
                'server.socket_port': 80,
                'log.screen': True,
                'engine.autoreload.on': False,
                'engine.SIGHUP': None,
                'engine.SIGTERM': None
                }
            })
        
        os.environ['DJANGO_SETTINGS_MODULE'] = 'mgp.settings'
        DjangoAppPlugin(cherrypy.engine, settings).subscribe()

        cherrypy.engine.start()
        cherrypy.engine.block()
        
    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        cherrypy.engine.exit()
        
        self.ReportServiceStatus(win32service.SERVICE_STOPPED)
        
if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(MyService)
    
