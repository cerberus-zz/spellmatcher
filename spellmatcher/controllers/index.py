#!/usr/bin/env python
#-*- coding:utf-8 -*-

from spellmatcher.controllers.base import Controller, route, url
from spellmatcher.models import RegisteredUser
from spellmatcher.models.feeds import *

class HomeController(Controller):

    def load_feeds(self):
        feed = Feed("http://twitter.com/statuses/user_timeline/77633129.rss")
        feed.load()

        return feed.items

    @route("/home")
    def index(self):
        return self.render_template("index.html", news=self.load_feeds(), registered=False)

    @route("/home/register")
    def register(self, username, email):
        new_user = RegisteredUser(username, email)
        self.context.save(new_user)

        return self.render_template("index.html", news=self.load_feeds(), name=username, email=email, registered=True)

#fica comentado só pra ter exemplos do url_for
#class OtherController(Controller):
#    @route("/other")
#    def index(self):
#        paths = []
#        paths.append(self.url_for(action="index"))
#        paths.append(self.url_for(url="something"))
#        paths.append(self.url_for(url="http://%s:%d" % (self.context.host, self.context.port)))
#        paths.append(self.url_for(url="http://www.globo.com"))
#        paths.append(self.url_for(controller="OtherController", action="index"))
#        paths.append(self.url_for(controller=OtherController, action="index"))
#        
#        links = ["<a href='%s'>%s</a>" % (action_url, action_url) for action_url in paths]
#        return self.render_to_response("<br />".join(links))

