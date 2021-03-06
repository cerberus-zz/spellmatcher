#!/usr/bin/env python
#-*- coding:utf-8 -*-

import sys
from os.path import abspath, join, dirname

import cherrypy

from spellmatcher.controllers import *
from spellmatcher.infra.context import SpellMatcherContext
from spellmatcher.infra.sqlalchemy_tool import metadata, session, mapper

class Server(object):
    @classmethod
    def __setup_routes(cls, context):
        d = cherrypy.dispatch.RoutesDispatcher()
        for controller_type in Controller.all():
            controller = controller_type()
            controller.context = context
            controller.register_routes(d)

        dispatcher = d
        return dispatcher


    @classmethod
    def start(cls):
        ctx = SpellMatcherContext(metadata=metadata, session=session, mapper=mapper)
        cherrypy.config.update({
                'server.socket_host': ctx.host,
                'server.socket_port': ctx.port,
                'tools.encode.on': True, 
                'tools.encode.encoding': 'utf-8',
                'tools.decode.on': True,
                'tools.trailing_slash.on': True,
                'tools.staticdir.root': ctx.static,
                'tools.SATransaction.on': True,
                'tools.SATransaction.dburi': ctx.db_connection,
                'tools.SATransaction.echo': False,
                'tools.SATransaction.convert_unicode': True,
                'log.screen': True,
                'tools.sessions.on': True
            })

        conf = {
            '/': {
                'request.dispatch': cls.__setup_routes(ctx),
            },
            '/media': {
                'tools.staticdir.on': True,
                'tools.staticdir.dir': 'media/' + ctx.template
            }
        }

        app = cherrypy.tree.mount(None, config=conf)
        
        cherrypy.quickstart(app)

    @classmethod
    def stop(cls):
        print "Killing skink..."
        cherrypy.engine.exit()
        print "skink killed."

if __name__ == '__main__':
    server = Server()
    sys.exit(server.start())

