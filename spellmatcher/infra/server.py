#!/usr/bin/env python
#-*- coding:utf-8 -*-

# Copyright Bernardo Heynemann <heynemann@gmail.com>

# Licensed under the Open Software License ("OSL") v. 3.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.opensource.org/licenses/osl-3.0.php

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys
from os.path import abspath, join, dirname

import cherrypy

from spellmatcher.controllers import *

class Server(object):
    @classmethod
    def __setup_routes(cls):
        d = cherrypy.dispatch.RoutesDispatcher()
        for controller_type in Controller.all():
            controller = controller_type()
            controller.register_routes(d)

        dispatcher = d
        return dispatcher


    @classmethod
    def start(cls):
        ctx = {
            "host":"0.0.0.0",
            "port":4000,
            "static_dir":abspath(join(dirname(__file__), "../"))
        }
        cherrypy.config.update({
                'server.socket_host': ctx["host"],
                'server.socket_port': ctx["port"],
                'tools.encode.on': True, 
                'tools.encode.encoding': 'utf-8',
                'tools.decode.on': True,
                'tools.trailing_slash.on': True,
                'tools.staticdir.root': ctx["static_dir"],
                'log.screen': True,
                'tools.sessions.on': True
            })

        conf = {
            '/': {
                'request.dispatch': cls.__setup_routes(),
            },
            '/media': {
                'tools.staticdir.on': True,
                'tools.staticdir.dir': 'media'
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

