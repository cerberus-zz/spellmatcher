#!/usr/bin/env python
#-*- coding:utf-8 -*-

import sys
from os.path import abspath, join, dirname

from genshi.template import TemplateLoader

class SpellMatcherContext(object):
    def __init__(self, **kw):
        root_dir = abspath(join(dirname(__file__), '../'))
        defaults = {
            'host':'127.0.0.1',
            'port':4000,
            'static': root_dir,
            'template_dir':join(root_dir,'templates'),
            'template':'default',
            'authenticated':False
        }

        defaults.update(kw)

        for k,v in defaults.iteritems():
            setattr(self, k, v)

        self.load_template_renderer()

    def load_template_renderer(self):
        self.loader = TemplateLoader(
            join(self.template_dir, self.template),
            auto_reload=True
        )


