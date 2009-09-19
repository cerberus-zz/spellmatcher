#!/usr/bin/env python
#-*- coding:utf-8 -*-

from spellmatcher.controllers.base import Controller, route, url

class HomeController(Controller):

    @route("/home")
    def index(self):
        paths = []
        paths.append(self.url_for(action="index"))
        paths.append(self.url_for(url="something"))
        paths.append(self.url_for(url="http://%s:%d" % (self.context.host, self.context.port)))
        paths.append(self.url_for(url="http://www.globo.com"))
        paths.append(self.url_for(controller="OtherController", action="index"))
        paths.append(self.url_for(controller=OtherController, action="index"))
        
        links = ["<a href='%s'>%s</a>" % (action_url, action_url) for action_url in paths]
        return self.render_to_response("<br />".join(links))

class OtherController(Controller):
    @route("/other")
    def index(self):
        paths = []
        paths.append(url.home.index())
        paths.append(url("something"))
        paths.append(url.other.index())
        
        links = ["<a href='%s'>%s</a>" % (action_url, action_url) for action_url in paths]
        return self.render_to_response("<br />".join(links))

