#!/usr/bin/env python
#-*- coding:utf-8 -*-

import routes
import cherrypy

__CONTROLLERS__ = []
__CONTROLLERSDICT__ = {}

def route(route, name=None):
    def dec(func):
        actual_name = func.__name__
        if name:
            actual_name = name
        conf = (
            actual_name, {
                'route': route,
                'method': func.__name__
            }
        )
        return func, conf

    return dec

class MetaController(type):
    def __init__(cls, name, bases, attrs):
        if name not in ('MetaController', 'Controller'):
            __CONTROLLERS__.append(cls)
            __CONTROLLERSDICT__[name] = cls
            cls.__routes__ = []
            for attr, value in attrs.items():
                if isinstance(value, tuple) and len(value) is 2:
                    method, conf = value
                    setattr(cls, attr, method)
                    cls.__routes__.append(conf)

        super(MetaController, cls).__init__(name, bases, attrs)

def get_controller_name(controller):
    return controller.lower().replace("controller", "")

def urlify(url):
    return url.startswith("http") and url or cherrypy.url(url)

class Controller(object):
    __metaclass__ = MetaController
    __routes__ = None
    context = None
    
    @classmethod
    def all(self):
        return __CONTROLLERS__

    def register_routes(self, dispatcher):
        for route in self.__routes__:
            route_name = "%s_%s" % (get_controller_name(self.__class__.__name__), route[0])
            dispatcher.connect(route_name, route[1]["route"], controller=self, action=route[1]["method"])
    
    def render_to_response(self, response):
        return response

    def url_for(self, controller=None, action=None, url=None, *args, **kw):
        if not controller:
            controller = self.__class__.__name__
        if isinstance(controller, type) and issubclass(controller, Controller):
            controller = controller.__name__

        if not action:
            return urlify(url)
        
        return urlify(routes.url_for(controller="%s_%s" % (get_controller_name(controller), action), *args, **kw))

class _ctrlchain(object):
 
    def __init__(self, name, head=None):
        if head is None:
            self.chain = list()
        else:
            self.chain = head[:]
        self.chain.append(name)
 
    def __getattr__(self, attr):
        return _ctrlchain(attr, self.chain)

    def __call__(self, *args, **kwargs):
        if len(self.chain) > 3:
            raise Exception("Don't know what to do with over 3 chain elements")
        if len(self.chain) > 2:
            action = self.chain[2]
        if len(self.chain) > 1:
            controller = self.chain[1]

        if len(args) == 1 and len(kwargs) == 0 and type(args[0]) in (str, unicode):
            return urlify(args[0])
        else:
            return urlify(routes.url_for(controller="%s_%s" % (get_controller_name(controller), action), *args, **kwargs))
 
url = _ctrlchain('urlgen')

