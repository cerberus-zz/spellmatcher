#!/usr/bin/env python
#-*- coding:utf-8 -*-

import sys
from os.path import abspath, join, dirname

class SpellMatcherContext(object):
    def __init__(self, **kw):
        defaults = {
            'host':'localhost',
            'port':4000,
            'static':abspath(join(dirname(__file__), '../'))
        }

        defaults.update(kw)

        for k,v in defaults.iteritems():
            setattr(self, k, v)
