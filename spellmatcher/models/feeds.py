#!/usr/bin/env python
#-*- coding:utf-8 -*-

import feedparser

class Feed(object):
    def __init__(self, url):
        self.url = url
        self.items = []

    def load(self):
        d = feedparser.parse(self.url)
        for entry in d.entries:
            item = FeedItem(title=entry.title, 
                            link=entry.link, 
                            date=entry.updated_parsed, 
                            str_date=entry.updated, 
                            content=entry.title_detail.value)
            self.items.append(item)

class FeedItem(object):
    def __init__(self, title, link, date, str_date, content):
        self.title = title
        self.content = content
        self.link = link
        self.date = date
        self.str_date = str_date
