#!/usr/bin/env python
#-*- coding:utf-8 -*-

import sys
from os.path import abspath, join, dirname
from ConfigParser import ConfigParser

from genshi.template import TemplateLoader

class SpellMatcherContext(object):
    def __init__(self, session=None, metadata=None, mapper=None, **kw):
        root_dir = abspath(join(dirname(__file__), '../'))

        config = ConfigParser()
        config.read(join(root_dir, "config.ini"))

        defaults = {
            'host':config.get("General", "host"),
            'port':int(config.get("General", "port")),
            'static': root_dir,
            'template_dir':join(root_dir,'templates'),
            'template':config.get("General", "current_template"),
            'webserver_verbose':config.get("General", "webserver_verbose"),
            'authenticated':False,
            'db_connection':config.get("Database", "db_connection"),
            'db_host':config.get("Database", "db_host"),
            'db_name':config.get("Database", "db_name"),
            'db_user':config.get("Database", "db_user"),
            'db_pass':config.get("Database", "db_pass"),
            'db_verbose':config.get("Database", "db_verbose"),
        }

        defaults.update(kw)

        for k,v in defaults.iteritems():
            setattr(self, k, v)

        self.session = session
        self.metadata = metadata
        self.mapper = mapper

        self.load_template_renderer()

    def load_template_renderer(self):
        self.loader = TemplateLoader(
            join(self.template_dir, self.template),
            auto_reload=True
        )

    def save(self, model):
        self.session.add(model)

    def query(self, *args, **kw):
        return self.session.query(*args, **kw)
